"""Unit tests for QueryClient."""
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from async_snowflake.endpoints.query import QueryResult


class TestQueryClient:
    """Unit tests for QueryClient."""

    @pytest.mark.asyncio
    async def test_lazy_loading(self, mock_client):
        """Test query client is created lazily."""
        from async_snowflake.endpoints.query import QueryClient
        query_client = mock_client.query
        assert isinstance(query_client, QueryClient)

    @pytest.mark.asyncio
    async def test_execute_async_sends_async_query_param(self, mock_client):
        """execute_async must send async=true as a query param, not a body field.

        Regression test for GitHub issue #4: Snowflake SQL API v2 rejects an
        ``asyncExecution`` body field with 400/391917. The async flag belongs in
        the query string.
        """
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json = MagicMock(return_value={"statementHandle": "01c5588a-abcd"})
        mock_client._http_client.request.return_value = response

        handle = await mock_client.query.execute_async("SELECT 1")

        assert handle == "01c5588a-abcd"

        _, kwargs = mock_client._http_client.request.call_args
        assert kwargs["params"] == {"async": "true"}
        assert "asyncExecution" not in kwargs["json"]
        assert kwargs["json"]["statement"] == "SELECT 1"

    @pytest.mark.asyncio
    async def test_get_status_running(self, mock_client):
        """get_status maps HTTP 202 to 'running' without crashing (issue #5).

        The SQL API returns no "status" field; the old code fed None into the
        required QueryStatus.state and raised a ValidationError.
        """
        resp = MagicMock(status_code=202)
        resp.raise_for_status = MagicMock()
        resp.json = MagicMock(
            return_value={"code": "333334", "message": "Asynchronous execution in progress."}
        )
        mock_client._http_client.request.return_value = resp

        status = await mock_client.query.get_status("01c-handle")

        assert status.state == "running"
        assert status.row_count is None

    @pytest.mark.asyncio
    async def test_get_status_success(self, mock_client):
        """get_status maps HTTP 200 to 'success' and reads numRows (issue #5)."""
        resp = MagicMock(status_code=200)
        resp.raise_for_status = MagicMock()
        resp.json = MagicMock(
            return_value={"code": "090001", "resultSetMetaData": {"numRows": 2}, "data": []}
        )
        mock_client._http_client.request.return_value = resp

        status = await mock_client.query.get_status("01c-handle")

        assert status.state == "success"
        assert status.row_count == 2

    @pytest.mark.asyncio
    async def test_get_results_parses_metadata_and_partitions(self, mock_client):
        """get_results reads resultSetMetaData and follows partitions (issue #6).

        The old code read non-existent top-level keys (columns/rowCount/status),
        so columns/row_count/query_state came back empty, and only the first
        partition's rows were returned.
        """
        main = MagicMock(status_code=200)
        main.raise_for_status = MagicMock()
        main.json = MagicMock(
            return_value={
                "resultSetMetaData": {
                    "numRows": 3,
                    "rowType": [{"name": "ID"}, {"name": "NAME"}],
                    "partitionInfo": [{"rowCount": 1}, {"rowCount": 2}],
                },
                "data": [["1", "a"]],
            }
        )
        part1 = MagicMock(status_code=200)
        part1.raise_for_status = MagicMock()
        part1.json = MagicMock(return_value={"data": [["2", "b"], ["3", "c"]]})
        mock_client._http_client.request.side_effect = [main, part1]

        result = await mock_client.query.get_results("01c-handle")

        assert result.columns == ["ID", "NAME"]
        assert result.row_count == 3
        assert result.query_state == "success"
        # first partition inline (1) + second partition fetched (2) == 3 rows
        assert result.rows == [["1", "a"], ["2", "b"], ["3", "c"]]
        # the second partition was fetched with ?partition=1
        _, part_kwargs = mock_client._http_client.request.call_args_list[1]
        assert part_kwargs["params"] == {"partition": 1}

    @pytest.mark.asyncio
    async def test_get_results_retries_transient_transport_error(self, mock_client):
        """A dropped keep-alive during a partition fetch is retried (issue #9).

        The first partition attempt raises RemoteProtocolError; get_results must
        retry and still return the complete result rather than aborting.
        """
        main = MagicMock(status_code=200)
        main.raise_for_status = MagicMock()
        main.json = MagicMock(
            return_value={
                "resultSetMetaData": {
                    "numRows": 3,
                    "rowType": [{"name": "ID"}, {"name": "NAME"}],
                    "partitionInfo": [{"rowCount": 1}, {"rowCount": 2}],
                },
                "data": [["1", "a"]],
            }
        )
        part1 = MagicMock(status_code=200)
        part1.raise_for_status = MagicMock()
        part1.json = MagicMock(return_value={"data": [["2", "b"], ["3", "c"]]})
        # initial GET ok; first partition attempt drops; retry succeeds
        mock_client._http_client.request.side_effect = [
            main,
            httpx.RemoteProtocolError("peer closed connection"),
            part1,
        ]

        with patch(
            "async_snowflake.endpoints.query.asyncio.sleep", new=AsyncMock()
        ) as sleep_mock:
            result = await mock_client.query.get_results("01c-handle")

        assert result.row_count == 3
        assert result.rows == [["1", "a"], ["2", "b"], ["3", "c"]]
        # one retry happened -> one backoff sleep, and three HTTP calls total
        sleep_mock.assert_awaited_once()
        assert mock_client._http_client.request.call_count == 3

    @pytest.mark.asyncio
    async def test_get_results_raises_after_retries_exhausted(self, mock_client):
        """Persistent transport failure re-raises after the retry budget (issue #9)."""
        main = MagicMock(status_code=200)
        main.raise_for_status = MagicMock()
        main.json = MagicMock(
            return_value={
                "resultSetMetaData": {
                    "numRows": 2,
                    "rowType": [{"name": "ID"}],
                    "partitionInfo": [{"rowCount": 1}, {"rowCount": 1}],
                },
                "data": [["1"]],
            }
        )
        mock_client._http_client.request.side_effect = [
            main,
            httpx.RemoteProtocolError("drop 1"),
            httpx.RemoteProtocolError("drop 2"),
            httpx.RemoteProtocolError("drop 3"),
        ]

        with patch("async_snowflake.endpoints.query.asyncio.sleep", new=AsyncMock()):
            with pytest.raises(httpx.RemoteProtocolError):
                await mock_client.query.get_results("01c-handle")

        # initial GET + 3 partition attempts (default attempts=3)
        assert mock_client._http_client.request.call_count == 4

    @pytest.mark.asyncio
    async def test_generate_results_streams_partition_batches(self, mock_client):
        """generate_results yields one partition (batch of rows) at a time, with retry."""
        main = MagicMock(status_code=200)
        main.raise_for_status = MagicMock()
        main.json = MagicMock(
            return_value={
                "resultSetMetaData": {
                    "rowType": [{"name": "N"}],
                    "partitionInfo": [{"rowCount": 1}, {"rowCount": 2}],
                },
                "data": [["1"]],
            }
        )
        part1 = MagicMock(status_code=200)
        part1.raise_for_status = MagicMock()
        part1.json = MagicMock(return_value={"data": [["2"], ["3"]]})
        # first partition attempt drops, retry succeeds
        mock_client._http_client.request.side_effect = [
            main,
            httpx.RemoteProtocolError("peer closed connection"),
            part1,
        ]

        batches = []
        with patch("async_snowflake.endpoints.query.asyncio.sleep", new=AsyncMock()):
            async for partition in mock_client.query.generate_results("01c-handle"):
                batches.append(partition)

        # one batch per partition (not flattened rows)
        assert batches == [[["1"]], [["2"], ["3"]]]
        # and flattening yields every row
        assert [row for batch in batches for row in batch] == [["1"], ["2"], ["3"]]


class TestQueryResult:
    """Unit tests for QueryResult class."""

    def test_iteration(self):
        """Test QueryResult iteration."""
        result = QueryResult(
            query_id="test_id",
            data=[["a", "b"], ["c", "d"]],
            columns=["col1", "col2"],
            row_count=2,
            status="success"
        )
        
        rows = list(result)
        assert len(rows) == 2

    def test_length(self):
        """Test QueryResult length."""
        result = QueryResult(
            query_id="test_id",
            data=[["a"], ["b"], ["c"]],
            columns=["col1"],
            row_count=3,
            status="success"
        )
        
        assert len(result) == 3
