'''
  Author: Jorge E. González Gonzalo
  Date: 2025-05-24
  GitHub: https://github.com/JK-GONZ

  Information:
    This file define a class create a file estructure
'''

from pathlib import Path
from typing import Dict, Optional, Union, List


class DirManager:
    '''Class to handle the file structure creation'''

    def __init__(self, base_path: Optional[Union[str, Path]] = None) -> None:
        self.base_path: Path = Path(base_path) if base_path else Path.cwd()
        self.structure: Dict[str, Dict] = {}
        self._tree_chars = ['│', '├', '└', '─', '│', '┌', '┐', '┘', '└']

    def _normalize_structure(self, structure_str: str) -> str:
        """Normalize the directory structure string by converting tree characters to spaces.

        Args
        ----
            structure_str: Raw directory structure string with tree characters

        Returns
        -------
            Normalized string with proper indentation
        """
        lines = []
        for line in structure_str.split('\n'):
            if not line.strip():
                continue

            # Count leading tree characters and convert to spaces
            indent = 0
            for char in line:
                if char in self._tree_chars or char == ' ':
                    indent += 1
                else:
                    break

            # Calculate proper indentation level (4 spaces per level)
            normalized_indent = (indent // 2) * 4
            # Clean the line content and maintain comments
            content = line[indent:].strip()

            # Add normalized line with proper indentation
            lines.append(' ' * normalized_indent + content)

        return '\n'.join(lines)

    def parse_structure(self, structure_str: str) -> None:
        """
            Parse a string representation of directory structure.
        """
        # Normalize the structure first
        normalized_str = self._normalize_structure(structure_str)

        lines = [line for line in normalized_str.split('\n') if line.strip()]
        if not lines:
            return

        # Process root directory
        self.structure = {lines[0].strip(): {}}

        # Process the rest of the structure recursively
        self._parse_level(lines[1:], list(self.structure.values())[0], 0)

    def _parse_level(self, lines: List[str], current_dict: Dict, parent_indent: int) -> int:
        """Process a level of the directory structure recursively."""
        i = 0
        last_dir = None
        last_indent = parent_indent

        while i < len(lines):
            line = lines[i]

            # Calculate real indent level based on spaces and tree characters
            raw_indent = len(line) - len(line.lstrip())
            indent_level = raw_indent // 4 * 4  # Normalize to blocks of 4 spaces

            # Check if we need to return to parent level
            if indent_level < parent_indent:
                return i

            # Extract directory name and clean it
            content = line.lstrip(' │├└─')
            parts = content.split('#', 1)
            dir_name = parts[0].strip().rstrip('/')

            if not dir_name:
                i += 1
                continue

            # Create new directory entry
            current_dict[dir_name] = {}

            # If this is a deeper level than previous, it's a child of last dir
            if indent_level > last_indent and last_dir is not None:
                current_dict = last_dir
            # If it's the same level, we stay in current dictionary
            elif indent_level == last_indent:
                last_dir = current_dict[dir_name]
            # If it's a shallower level, we've returned from a deeper structure
            else:
                last_dir = current_dict[dir_name]

            # Process next level if there are more lines
            next_idx = i + 1
            if next_idx < len(lines):
                next_indent = len(lines[next_idx]) - \
                    len(lines[next_idx].lstrip())
                if next_indent > indent_level:
                    processed = self._parse_level(
                        lines[next_idx:], current_dict[dir_name], next_indent)
                    i += processed

            last_indent = indent_level
            i += 1

        return i

    def create_directories(self, path: Optional[Union[str, Path]] = None) -> None:
        """Create the directory structure at the specified path or base_path."""
        if path:
            self.base_path = Path(path)

        def create_recursive(structure: Dict[str, Dict], current_path: Path) -> None:
            for name, subdir in structure.items():
                dir_path = current_path / name
                dir_path.mkdir(parents=True, exist_ok=True)
                create_recursive(subdir, dir_path)

        create_recursive(self.structure, self.base_path)

    def set_base_path(self, path: Union[str, Path]) -> None:
        """Set a new base path for directory creation.

        Args:
            path: New base path
        """
        self.base_path = Path(path)

    def preview_structure(self) -> str:
        """Generate a tree-like visualization of the directory structure."""
        def _build_tree(structure: Dict[str, Dict], prefix: str = '') -> str:
            lines = []
            items = list(structure.items())

            for i, (name, subdir) in enumerate(items):
                is_last_item = i == len(items) - 1
                connector = '└── ' if is_last_item else '├── '
                lines.append(f"{prefix}{connector}{name}")

                if subdir:
                    extension = '    ' if is_last_item else '│   '
                    sub_tree = _build_tree(subdir, prefix + extension)
                    lines.append(sub_tree)

            return '\n'.join(lines)

        return _build_tree(self.structure)
