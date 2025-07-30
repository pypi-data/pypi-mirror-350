import requests
import base64
from typing import Dict, Any,Literal

from ..models.tool_server_models import (
    MoveMouseRequest,
    ClickMouseRequest,
    PressMouseRequest,
    ReleaseMouseRequest,
    DragMouseRequest,
    ScrollRequest,
    PressKeyRequest,
    TypeTextRequest,
    WaitRequest,
    TakeScreenshotRequest,
    GetCursorPositionRequest,
    GetScreenSizeRequest,
    ChangePasswordRequest,
    BaseResponse,
    CursorPositionResponse,
    ScreenSizeResponse,
    ScreenshotResponse,
    ReadFileRequest,
    ReadFileResponse,
    ReadMultiFilesRequest,
    ReadMultiFilesResponse,
    ListDirectoryRequest,
    ListDirectoryResponse,
    SearchFileRequest,
    SearchFileResponse,
    SearchCodeResponse,
    GetFileInfoResponse,
    SearchCodeRequest,
    GetFileInfoRequest,
    CreateFileRequest,
    CreateFileResponse,
    ListSessionsRequest,
    ListSessionsResponse,
    ListProcessesRequest,
    ListProcessesResponse,
    ExecuteCommandRequest,
    ExecuteCommandResponse,
    FileOperationRequest,
    FileOperationResponse,
)

from ..models.common import (
    ComputerActionArgs,
    Action,
)

class ToolServerClient:
    """
    Client SDK for Computer Use Tool Server
    """

    def __init__(self, base_url: str, api_version: str = "2020-04-01"):
        """
        Initialize the Computer Use SDK client
        
        Args:
            base_url: Base URL of the Computer Use Tool Server
            api_version: API version to use
        """
        self.base_url = base_url
        self.api_version = api_version
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _make_request(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Computer Use Tool Server
        
        Args:
            action: Action to perform
            params: Parameters for the action
            
        Returns:
            Response from the server
        """
        url = self.base_url
        response = requests.get(url, params={**params, "Version": self.api_version, "Action": action}, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def move_mouse(self, x: int, y: int) -> BaseResponse:
        """
        Move the mouse to the specified position
        
        Args:
            x: X position
            y: Y position
            
        Returns:
            Response from the server
        """
        request = MoveMouseRequest(PositionX=x, PositionY=y)
        response_data = self._make_request("MoveMouse", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def click_mouse(
            self,
            x: int,
            y: int,
            button: Literal["left", "right", "middle", "double_click", "double_left"] = "left",
            press: bool = False,
            release: bool = False
    ) -> BaseResponse:
        """
        Click the mouse at the specified position
        
        Args:
            x: X position
            y: Y position
            button: Mouse button to click
            press: Whether to press the mouse button
            release: Whether to release the mouse button
            
        Returns:
            Response from the server
        """
        request = ClickMouseRequest(
            PositionX=x,
            PositionY=y,
            button=button,
            press=press,
            release=release
        )
        response_data = self._make_request("ClickMouse", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def press_mouse(
            self,
            x: int,
            y: int,
            button: Literal["left", "right", "middle"] = "left"
    ) -> BaseResponse:
        """
        Press the mouse button at the specified position
        
        Args:
            x: X position
            y: Y position
            button: Mouse button to press
            
        Returns:
            Response from the server
        """
        request = PressMouseRequest(
            PositionX=x,
            PositionY=y,
            button=button
        )
        response_data = self._make_request("PressMouse", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def release_mouse(
            self,
            x: int,
            y: int,
            button: Literal["left", "right", "middle"] = "left"
    ) -> BaseResponse:
        """
        Release the mouse button at the specified position
        
        Args:
            x: X position
            y: Y position
            button: Mouse button to release
            
        Returns:
            Response from the server
        """
        request = ReleaseMouseRequest(
            PositionX=x,
            PositionY=y,
            button=button
        )
        response_data = self._make_request("ReleaseMouse", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def drag_mouse(
            self,
            source_x: int,
            source_y: int,
            target_x: int,
            target_y: int
    ) -> BaseResponse:
        """
        Drag the mouse from source to target position
        
        Args:
            source_x: Source X position
            source_y: Source Y position
            target_x: Target X position
            target_y: Target Y position
            
        Returns:
            Response from the server
        """
        request = DragMouseRequest(
            source_x=source_x,
            source_y=source_y,
            target_x=target_x,
            target_y=target_y
        )
        response_data = self._make_request("DragMouse", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def scroll(
            self,
            x: int,
            y: int,
            scroll_direction: Literal["up", "down", "left", "right"] = "up",
            scroll_amount: int = 1
    ) -> BaseResponse:
        """
        Scroll at the specified position
        
        Args:
            x: X position
            y: Y position
            scroll_direction: Direction to scroll
            scroll_amount: Amount to scroll
            
        Returns:
            Response from the server
        """
        request = ScrollRequest(
            PositionX=x,
            PositionY=y,
            scroll_direction=scroll_direction,
            scroll_amount=scroll_amount
        )
        response_data = self._make_request("Scroll", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def press_key(self, key: str) -> BaseResponse:
        """
        Press the specified key
        
        Args:
            key: Key to press
            
        Returns:
            Response from the server
        """
        request = PressKeyRequest(key=key)
        response_data = self._make_request("PressKey", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def type_text(self, text: str) -> BaseResponse:
        """
        Type the specified text
        
        Args:
            text: Text to type
            
        Returns:
            Response from the server
        """
        request = TypeTextRequest(text=text)
        response_data = self._make_request("TypeText", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def wait(self, duration: int) -> BaseResponse:
        """
        Wait for the specified duration in milliseconds
        
        Args:
            duration: Duration to wait in milliseconds
            
        Returns:
            Response from the server
        """
        request = WaitRequest(duration=duration)
        response_data = self._make_request("Wait", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def take_screenshot(self) -> ScreenshotResponse:
        """
        Take a screenshot
        
        Returns:
            Response from the server with screenshot data
        """
        request = TakeScreenshotRequest()
        response_data = self._make_request("TakeScreenshot", request.model_dump(by_alias=True))
        return ScreenshotResponse(**response_data)

    def get_cursor_position(self) -> CursorPositionResponse:
        """
        Get the current cursor position
        
        Returns:
            Response containing cursor position in Result.x and Result.y
        """
        request = GetCursorPositionRequest()
        response_data = self._make_request("GetCursorPosition", request.model_dump(by_alias=True))
        return CursorPositionResponse(**response_data)

    def get_screen_size(self) -> ScreenSizeResponse:
        """
        Get the screen size
        
        Returns:
            Response containing screen size in Result.width and Result.height
        """
        request = GetScreenSizeRequest()
        response_data = self._make_request("GetScreenSize", request.model_dump(by_alias=True))
        print(response_data)
        return ScreenSizeResponse(**response_data)

    def change_password(self, username: str, new_password: str) -> BaseResponse:
        """
        Change the password for the specified user
        
        Args:
            username: Username
            new_password: New password
            
        Returns:
            Response from the server
        """
        request = ChangePasswordRequest(
            Username=username,
            NewPassword=new_password
        )
        response_data = self._make_request("ChangePassword", request.model_dump(by_alias=True))
        return BaseResponse(**response_data)

    def read_file(self, file_path: str) -> ReadFileResponse:
        """
        Read the content of a file

        Args:
            file_path: Path to the file

        Returns:
            Response containing the file content in Result.content
        """
        request = ReadFileRequest(file_path=file_path)
        response_data = self._make_request("ReadFile", request.model_dump(by_alias=True))
        return ReadFileResponse(**response_data)._decode_content()

    def read_multi_files(self, file_paths: list[str]) -> ReadMultiFilesResponse:
        """
        Read the content of multiple files
        Args:
            file_paths: List of paths to the files
        Returns:
            Response containing the file contents in Result.contents
        """
        request = ReadMultiFilesRequest(file_paths=file_paths)
        response_data = self._make_request("ReadMultiFiles", request.model_dump(by_alias=True))
        return ReadMultiFilesResponse(**response_data)._decode_content()

    def list_directory(self, dir_path: str) -> ListDirectoryResponse:
        """
        List the files in a directory
        Args:
            dir_path: Path to the directory
        Returns:
            Response containing the list of files in Result.files
        """
        request = ListDirectoryRequest(dir_path=dir_path)
        response_data = self._make_request("ListDirectory", request.model_dump(by_alias=True))
        print(f"list_directory response: {response_data}")
        return ListDirectoryResponse(**response_data)

    def search_file(self, dir_path: str, pattern: str) -> SearchFileResponse:
        """
        Search for files in a directory
        Args:
            dir_path: Path to the directory
            pattern: Pattern to search for
        Returns:
            Response containing the list of files in Result.files
        """
        request = SearchFileRequest(dir_path=dir_path, pattern=pattern)
        response_data = self._make_request("SearchFile", request.model_dump(by_alias=True))
        return SearchFileResponse(**response_data)

    def search_code(self, file_path: str, pattern: str) -> SearchCodeResponse:
        """
        Search for code in a file
        Args:
            file_path: Path to the file
            pattern: Pattern to search for
        Returns:
            Response containing the code in Result.content
        """
        request = SearchCodeRequest(file_path=file_path, pattern=pattern)
        response_data = self._make_request("SearchCode", request.model_dump(by_alias=True))
        return SearchCodeResponse(**response_data)

    def get_file_info(self, file_path: str) -> GetFileInfoResponse:
        """
        Get information about a file
        Args:
            file_path: Path to the file
        Returns:
            Response containing the file information in Result.info
        """
        request = GetFileInfoRequest(file_path=file_path)
        response_data = self._make_request("GetFileInfo", request.model_dump(by_alias=True))
        return GetFileInfoResponse(**response_data)

    def create_file(self, file_path: str, content: bytes) -> CreateFileResponse:
        """
        Create a file
        Args:
            file_path: Path to the file
            content: Content of the file
        Returns:
            Response containing the file information in Result.info
        """
        request = CreateFileRequest(file_path=file_path, content=base64.encodebytes(content))
        response_data = self._make_request("CreateFile", request.model_dump(by_alias=True))
        return CreateFileResponse(**response_data)

    def list_sessions(self) -> ListSessionsResponse:
        """
        List the sessions of terminals
        Returns:
            Response containing the list of sessions in Result.output
        """
        request = ListSessionsRequest()
        response_data = self._make_request("ListSessions", request.model_dump(by_alias=True))
        return ListSessionsResponse(**response_data)

    def list_processes(self) -> ListProcessesResponse:
        """
        List the processes
        Returns:
            Response containing the list of processes in Result.processes
        """
        request = ListProcessesRequest()
        response_data = self._make_request("ListProcesses", request.model_dump(by_alias=True))
        return ListProcessesResponse(**response_data)

    def execute_command(self, **params) -> ExecuteCommandResponse:
        """
        Execute a bash command

        Args:
            **params: Parameters for the bash command

        Returns:
            Response from the server
        """
        params = ExecuteCommandRequest.model_validate(params).model_dump(by_alias=True, exclude_unset=True)
        response_data = self._make_request("ExecuteCommand", params)
        return ExecuteCommandResponse(**response_data)
    
    def file_operation(self, **params) -> FileOperationResponse:
        """
        Execute a file operation
        Args:
            **params: Parameters for the file operation
        Returns:
            Response from the server
        """
        params = FileOperationRequest.model_validate(params).encde_content().model_dump(by_alias=True, exclude_unset=True)
        response_data = self._make_request("FileOperation", params)
        return FileOperationResponse(**response_data).decode_content()

    async def computer_action(self, action: ComputerActionArgs, **kwargs) -> BaseResponse:
        """
        Perform a computer action
        Args:
            action: Action to perform
            **kwargs: Additional arguments for the action
        Returns:
            Response from the server
        """
        if action.action == Action.MOVE_MOUSE:
            return self.move_mouse(action.coordinates[0], action.coordinates[1])
        elif action.action == Action.CLICK_MOUSE:
            return self.click_mouse(action.coordinates[0], action.coordinates[1], action.button, action.press, action.release)
        elif action.action == Action.PRESS_KEY:
            return self.press_key(action.keys[0] if len(action.keys) == 1 else " ".join(action.keys))
        elif action.action == Action.TYPE_TEXT:
            return self.type_text(action.text)
        elif action.action == Action.WAIT:
            return self.wait(action.duration)
        elif action.action == Action.TAKE_SCREENSHOT:
            return self.take_screenshot()
        elif action.action == Action.SCROLL:
            return self.scroll(action.coordinates[0], action.coordinates[1], action.scroll_direction, action.scroll_amount)
        elif action.action == Action.DRAG_MOUSE:
            return self.drag_mouse(action.coordinates[0], action.coordinates[1], action.coordinates[2], action.coordinates[3])
        return BaseResponse()

def new_computer_use_client(endpoint: str) -> ToolServerClient:
    return ToolServerClient(base_url=endpoint)