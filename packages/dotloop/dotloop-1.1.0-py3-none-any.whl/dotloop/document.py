"""Document client for the Dotloop API wrapper."""

from typing import Any, Dict, Optional, Union
import io

from .base_client import BaseClient


class DocumentClient(BaseClient):
    """Client for document API endpoints."""

    def list_documents(self, profile_id: int, loop_id: int) -> Dict[str, Any]:
        """List all documents in a loop.

        Args:
            profile_id: ID of the profile
            loop_id: ID of the loop

        Returns:
            Dictionary containing list of documents with metadata

        Raises:
            DotloopError: If the API request fails
            NotFoundError: If the loop is not found

        Example:
            ```python
            documents = client.document.list_documents(profile_id=123, loop_id=456)
            for document in documents['data']:
                print(f"Document: {document['name']} (ID: {document['id']})")
            ```
        """
        return self.get(f"/profile/{profile_id}/loop/{loop_id}/document")

    def get_document(self, profile_id: int, loop_id: int, document_id: int) -> Dict[str, Any]:
        """Retrieve an individual document by ID.

        Args:
            profile_id: ID of the profile
            loop_id: ID of the loop
            document_id: ID of the document to retrieve

        Returns:
            Dictionary containing document information including metadata and download URL

        Raises:
            DotloopError: If the API request fails
            NotFoundError: If the document is not found

        Example:
            ```python
            document = client.document.get_document(
                profile_id=123, 
                loop_id=456, 
                document_id=789
            )
            print(f"Document: {document['data']['name']}")
            print(f"Download URL: {document['data']['downloadUrl']}")
            ```
        """
        return self.get(f"/profile/{profile_id}/loop/{loop_id}/document/{document_id}")

    def upload_document(
        self,
        profile_id: int,
        loop_id: int,
        file_content: Union[bytes, io.IOBase],
        filename: str,
        folder_id: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload a document to a loop.

        Args:
            profile_id: ID of the profile
            loop_id: ID of the loop
            file_content: File content as bytes or file-like object
            filename: Name of the file
            folder_id: ID of the folder to upload to (optional)
            description: Description of the document (optional)

        Returns:
            Dictionary containing uploaded document information

        Raises:
            DotloopError: If the API request fails
            ValidationError: If parameters are invalid

        Example:
            ```python
            # Upload from file
            with open("contract.pdf", "rb") as f:
                document = client.document.upload_document(
                    profile_id=123,
                    loop_id=456,
                    file_content=f.read(),
                    filename="contract.pdf",
                    description="Purchase contract"
                )
            
            # Upload to specific folder
            document = client.document.upload_document(
                profile_id=123,
                loop_id=456,
                file_content=file_bytes,
                filename="inspection_report.pdf",
                folder_id=789,
                description="Home inspection report"
            )
            ```
        """
        import requests
        from urllib.parse import urljoin

        # Build URL
        url = self._build_url(f"/profile/{profile_id}/loop/{loop_id}/document")
        
        # Prepare headers (exclude Content-Type for multipart)
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
        }

        # Prepare form data
        files = {"file": (filename, file_content)}
        data = {}
        
        if folder_id is not None:
            data["folderId"] = str(folder_id)
        if description is not None:
            data["description"] = description

        try:
            response = requests.post(
                url,
                files=files,
                data=data,
                headers=headers,
                timeout=self._timeout
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            from .exceptions import DotloopError
            raise DotloopError(f"Request failed: {str(e)}")

    def upload_document_from_file(
        self,
        profile_id: int,
        loop_id: int,
        file_path: str,
        folder_id: Optional[int] = None,
        description: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload a document from a file path.

        Args:
            profile_id: ID of the profile
            loop_id: ID of the loop
            file_path: Path to the file to upload
            folder_id: ID of the folder to upload to (optional)
            description: Description of the document (optional)
            filename: Custom filename (optional, defaults to file basename)

        Returns:
            Dictionary containing uploaded document information

        Raises:
            DotloopError: If the API request fails
            FileNotFoundError: If the file doesn't exist
            ValidationError: If parameters are invalid

        Example:
            ```python
            document = client.document.upload_document_from_file(
                profile_id=123,
                loop_id=456,
                file_path="/path/to/contract.pdf",
                description="Purchase contract"
            )
            ```
        """
        import os
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if filename is None:
            filename = os.path.basename(file_path)
        
        with open(file_path, "rb") as f:
            return self.upload_document(
                profile_id=profile_id,
                loop_id=loop_id,
                file_content=f,
                filename=filename,
                folder_id=folder_id,
                description=description,
            )

    def download_document(
        self, 
        profile_id: int, 
        loop_id: int, 
        document_id: int
    ) -> bytes:
        """Download a document's content.

        Args:
            profile_id: ID of the profile
            loop_id: ID of the loop
            document_id: ID of the document to download

        Returns:
            Document content as bytes

        Raises:
            DotloopError: If the API request fails
            NotFoundError: If the document is not found

        Example:
            ```python
            # Download document content
            content = client.document.download_document(
                profile_id=123,
                loop_id=456,
                document_id=789
            )
            
            # Save to file
            with open("downloaded_document.pdf", "wb") as f:
                f.write(content)
            ```
        """
        import requests
        
        # First get document info to get download URL
        document_info = self.get_document(profile_id, loop_id, document_id)
        download_url = document_info['data'].get('downloadUrl')
        
        if not download_url:
            from .exceptions import DotloopError
            raise DotloopError("Document download URL not available")
        
        # Download the file content
        headers = {
            "Authorization": f"Bearer {self._api_key}",
        }
        
        try:
            response = requests.get(download_url, headers=headers, timeout=self._timeout)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            from .exceptions import DotloopError
            raise DotloopError(f"Download failed: {str(e)}")

    def download_document_to_file(
        self,
        profile_id: int,
        loop_id: int,
        document_id: int,
        file_path: str,
    ) -> None:
        """Download a document and save it to a file.

        Args:
            profile_id: ID of the profile
            loop_id: ID of the loop
            document_id: ID of the document to download
            file_path: Path where to save the downloaded file

        Raises:
            DotloopError: If the API request fails
            NotFoundError: If the document is not found

        Example:
            ```python
            client.document.download_document_to_file(
                profile_id=123,
                loop_id=456,
                document_id=789,
                file_path="/path/to/save/document.pdf"
            )
            ```
        """
        content = self.download_document(profile_id, loop_id, document_id)
        
        with open(file_path, "wb") as f:
            f.write(content) 