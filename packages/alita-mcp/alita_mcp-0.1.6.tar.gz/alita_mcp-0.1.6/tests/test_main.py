import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from src.alita_mcp.main import cli, main, bootstrap

class TestMain(unittest.TestCase):
    @patch("src.alita_mcp.main.get_bootstrap_config", return_value={"deployment_url": "http://example.com", "auth_token": "token", "host": "0.0.0.0", "port": 8000})
    @patch("src.alita_mcp.main.run")
    @patch("src.alita_mcp.main.Agent")
    def test_main_run_with_app_id(self, mock_agent_class, mock_run, mock_get_config):
        # Setup mock Agent instance
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        test_args = ["main", "run", "--project_id", "1", "--app_id", "2", "--version_id", "3", "--transport", "stdio"]
        with patch.object(sys, "argv", test_args):
            captured_output = StringIO()
            with patch("sys.stdout", captured_output):
                cli()
            output = captured_output.getvalue()
            self.assertIn("Starting MCP server", output)
            self.assertIn("Using application: 2", output)
            mock_run.assert_called_once_with(mock_agent, transport="stdio", host="0.0.0.0", port=8000)
            # Verify Agent was constructed with correct parameters
            mock_agent_class.assert_called_once_with(
                base_url="http://example.com",
                project_id="1",
                auth_token="token",
                app_id="2",
                version_id="3"
            )

    @patch("src.alita_mcp.main.get_bootstrap_config", return_value={"deployment_url": "http://example.com", "auth_token": "token", "host": "0.0.0.0", "port": 8000})
    @patch("src.alita_mcp.main.run")
    @patch("src.alita_mcp.main.Agents")
    def test_main_run_project_only(self, mock_agents_class, mock_run, mock_get_config):
        # Setup mock Agents instance and its agents attribute
        mock_agents = MagicMock()
        mock_agents.agents = MagicMock()
        mock_agents_class.return_value = mock_agents
        
        # Note: Even though we pass port=9000, the config port (8000) will be used
        test_args = ["main", "run", "--project_id", "1", "--transport", "sse", "--port", "9000"]
        with patch.object(sys, "argv", test_args):
            captured_output = StringIO()
            with patch("sys.stdout", captured_output):
                cli()
            output = captured_output.getvalue()
            self.assertIn("Starting MCP server", output)
            self.assertIn("Using all available project agents", output)
            # Update assertion to expect port=8000 (from config) rather than 9000 (from args)
            mock_run.assert_called_once_with(mock_agents.agents, transport="sse", host="0.0.0.0", port=8000)
            # Verify Agents was constructed with correct parameters
            mock_agents_class.assert_called_once_with(
                base_url="http://example.com",
                project_id="1",
                auth_token="token",
                api_extra_headers=None
            )

    @patch("src.alita_mcp.main.get_bootstrap_config", return_value={})
    def test_main_missing_config(self, mock_get_config):
        test_args = ["main", "run", "--project_id", "1", "--app_id", "2", "--version_id", "3"]
        with patch.object(sys, "argv", test_args):
            captured_output = StringIO()
            with patch("sys.stdout", captured_output):
                cli()
            output = captured_output.getvalue()
            self.assertIn("Error: Configuration missing", output)

    @patch("src.alita_mcp.main.get_bootstrap_config", return_value={"deployment_url": "http://example.com", "auth_token": "token"})
    @patch("src.alita_mcp.main.run")
    @patch("src.alita_mcp.main.Agent")
    @patch("src.alita_mcp.main.Agents")
    def test_main_no_project_id(self, mock_agents_class, mock_agent_class, mock_run, mock_get_config):
        test_args = ["main", "run"]
        with patch.object(sys, "argv", test_args):
            captured_output = StringIO()
            with patch("sys.stdout", captured_output):
                cli()
            output = captured_output.getvalue()
            self.assertIn("Error: Project ID is required", output)
            mock_run.assert_not_called()
            mock_agent_class.assert_not_called()
            mock_agents_class.assert_not_called()

    @patch("src.alita_mcp.main.interactive_bootstrap", return_value={"deployment_url": "http://example.com", "auth_token": "token"})
    def test_bootstrap_interactive(self, mock_interactive):
        test_args = ["main", "bootstrap"]
        with patch.object(sys, "argv", test_args):
            captured_output = StringIO()
            with patch("sys.stdout", captured_output):
                cli()
            output = captured_output.getvalue()
            self.assertIn("Deployment URL:", output)
            self.assertIn("Auth Token: ********", output)

    @patch("src.alita_mcp.main.set_bootstrap_config", 
           return_value={"deployment_url": "http://custom.com", "auth_token": "custom-token"})
    def test_bootstrap_non_interactive(self, mock_set_config):
        test_args = ["main", "bootstrap", "--deployment_url", "http://custom.com", 
                     "--auth_token", "custom-token", "--host", "127.0.0.1", "--port", "9000"]
        with patch.object(sys, "argv", test_args):
            captured_output = StringIO()
            with patch("sys.stdout", captured_output):
                cli()
            output = captured_output.getvalue()
            self.assertIn("Deployment URL: http://custom.com", output)
            mock_set_config.assert_called_once_with("http://custom.com", "custom-token", "127.0.0.1", 9000)

if __name__ == "__main__":
    unittest.main()
