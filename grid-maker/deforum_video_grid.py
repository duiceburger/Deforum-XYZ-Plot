#!/usr/bin/env python3
"""
Deforum Video Grid Generator

Creates video grids from Deforum batch outputs, similar to Automatic1111's image grids
but for video files. Automatically detects X/Y parameter structure and arranges videos
in a grid layout.

Usage:
    python deforum_video_grid.py [batch_directory] [options]

Requirements:
    - FFmpeg installed and accessible in PATH
    - Python 3.6+
"""

import os
import sys
import re
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import tempfile
import platform

class FFmpegLocator:
    """Locate FFmpeg executable across different systems and installation types."""
    
    @staticmethod
    def find_ffmpeg() -> Optional[str]:
        """Find FFmpeg executable using multiple detection strategies."""
        print("=== FFmpeg Detection Debug ===")
        
        # Strategy 1: Check Automatic1111 installations first
        print("Strategy 1: Checking A1111 installations...")
        a1111_ffmpeg = FFmpegLocator._find_a1111_ffmpeg()
        if a1111_ffmpeg:
            print(f"SUCCESS: Found A1111 FFmpeg at: {a1111_ffmpeg}")
            return a1111_ffmpeg
        print("Strategy 1: No A1111 FFmpeg found")
        
        # Strategy 2: Check PATH
        print("Strategy 2: Checking system PATH...")
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, check=True, timeout=5)
            print(f"SUCCESS: Found FFmpeg in PATH")
            return 'ffmpeg'
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"Strategy 2: PATH check failed: {type(e).__name__}")
        
        # Strategy 3: Common installation paths by OS
        print("Strategy 3: Checking common installation paths...")
        common_paths = FFmpegLocator._get_common_paths()
        
        for path in common_paths:
            print(f"  Checking: {path}")
            ffmpeg_path = Path(path)
            if ffmpeg_path.exists() and ffmpeg_path.is_file():
                try:
                    result = subprocess.run([str(ffmpeg_path), '-version'], 
                                          capture_output=True, check=True, timeout=5)
                    print(f"SUCCESS: Found working FFmpeg at: {path}")
                    return str(ffmpeg_path)
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                    print(f"  Failed version check: {type(e).__name__}")
                    continue
            else:
                print(f"  Not found or not a file")
        
        # Strategy 4: Search common directories
        print("Strategy 4: Searching common directories...")
        search_dirs = FFmpegLocator._get_search_directories()
        
        for search_dir in search_dirs:
            print(f"  Searching directory: {search_dir}")
            if not Path(search_dir).exists():
                print(f"    Directory does not exist")
                continue
                
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if FFmpegLocator._is_ffmpeg_executable(file):
                        candidate = Path(root) / file
                        print(f"    Found candidate: {candidate}")
                        try:
                            result = subprocess.run([str(candidate), '-version'], 
                                                  capture_output=True, check=True, timeout=5)
                            print(f"SUCCESS: Found working FFmpeg at: {candidate}")
                            return str(candidate)
                        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                            print(f"    Failed version check: {type(e).__name__}")
                            continue
        
        print("FAILURE: No working FFmpeg found")
        return None
    
    @staticmethod
    def _find_a1111_ffmpeg() -> Optional[str]:
        """Specifically search for Automatic1111 FFmpeg installations."""
        current_path = Path.cwd()
        print(f"  Current working directory: {current_path}")
        
        # Search up the directory tree for stable-diffusion-webui
        for i in range(5):  # Search up to 5 levels
            print(f"  Level {i}: Checking {current_path}")
            
            webui_path = current_path / 'stable-diffusion-webui'
            print(f"    Looking for webui at: {webui_path}")
            if webui_path.exists():
                ffmpeg_path = webui_path / 'ffmpeg.exe'
                print(f"    Checking FFmpeg at: {ffmpeg_path}")
                if ffmpeg_path.exists():
                    try:
                        result = subprocess.run([str(ffmpeg_path), '-version'], 
                                             capture_output=True, check=True, timeout=5)
                        print(f"    SUCCESS: Working FFmpeg found")
                        return str(ffmpeg_path)
                    except Exception as e:
                        print(f"    Failed version check: {type(e).__name__}: {e}")
                else:
                    print(f"    FFmpeg not found at expected location")
            else:
                print(f"    Webui directory not found")
            
            # Check if current directory is the webui directory
            if current_path.name == 'stable-diffusion-webui':
                ffmpeg_path = current_path / 'ffmpeg.exe'
                print(f"    Current dir is webui, checking: {ffmpeg_path}")
                if ffmpeg_path.exists():
                    try:
                        result = subprocess.run([str(ffmpeg_path), '-version'], 
                                             capture_output=True, check=True, timeout=5)
                        print(f"    SUCCESS: Working FFmpeg found in webui root")
                        return str(ffmpeg_path)
                    except Exception as e:
                        print(f"    Failed version check: {type(e).__name__}: {e}")
                else:
                    print(f"    FFmpeg not found in webui root")
            
            current_path = current_path.parent
            if current_path == current_path.parent:  # Reached root
                print(f"    Reached filesystem root")
                break
        
        # Check common A1111 installation paths
        print("  Checking common A1111 installation paths...")
        a1111_common_paths = [
            # Direct FFmpeg executables
            'D:/AI Apps/stable-diffusion-webui/ffmpeg.exe',
            'C:/stable-diffusion-webui/ffmpeg.exe',
            'D:/stable-diffusion-webui/ffmpeg.exe',
            'E:/stable-diffusion-webui/ffmpeg.exe',
            # ImageIO FFmpeg binaries (common location)
            'D:/AI Apps/stable-diffusion-webui/venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe',
            'C:/stable-diffusion-webui/venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe',
            'D:/stable-diffusion-webui/venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe',
            'E:/stable-diffusion-webui/venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe',
        ]
        
        for path in a1111_common_paths:
            print(f"    Checking: {path}")
            ffmpeg_path = Path(path)
            if ffmpeg_path.exists():
                try:
                    result = subprocess.run([str(ffmpeg_path), '-version'], 
                                         capture_output=True, check=True, timeout=5)
                    print(f"    SUCCESS: Working FFmpeg found")
                    return str(ffmpeg_path)
                except Exception as e:
                    print(f"    Failed version check: {type(e).__name__}: {e}")
                    continue
            else:
                print(f"    File does not exist")
        
        print("  No A1111 FFmpeg installations found")
        return None
    
    @staticmethod
    def _get_common_paths() -> List[str]:
        """Get OS-specific common FFmpeg installation paths."""
        system = platform.system().lower()
        
        if system == 'windows':
            return [
                'C:/ffmpeg/bin/ffmpeg.exe',
                'C:/Program Files/ffmpeg/bin/ffmpeg.exe',
                'C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe',
                str(Path.home() / 'ffmpeg/bin/ffmpeg.exe'),
                'D:/ffmpeg/bin/ffmpeg.exe',
            ]
        elif system == 'darwin':  # macOS
            return [
                '/usr/local/bin/ffmpeg',
                '/opt/homebrew/bin/ffmpeg',
                '/usr/bin/ffmpeg',
                str(Path.home() / 'bin/ffmpeg'),
            ]
        else:  # Linux and others
            return [
                '/usr/bin/ffmpeg',
                '/usr/local/bin/ffmpeg',
                '/snap/bin/ffmpeg',
                str(Path.home() / 'bin/ffmpeg'),
                str(Path.home() / '.local/bin/ffmpeg'),
            ]
    
    @staticmethod
    def _get_search_directories() -> List[str]:
        """Get directories to search for FFmpeg."""
        system = platform.system().lower()
        
        base_dirs = [str(Path.home())]
        
        if system == 'windows':
            base_dirs.extend([
                'C:/Program Files',
                'C:/Program Files (x86)',
                'C:/',
                'D:/',
            ])
        else:
            base_dirs.extend([
                '/usr/local',
                '/opt',
                '/usr',
            ])
        
        return base_dirs
    
    @staticmethod
    def _is_ffmpeg_executable(filename: str) -> bool:
        """Check if filename matches FFmpeg executable patterns."""
        system = platform.system().lower()
        
        if system == 'windows':
            return filename.lower() in ['ffmpeg.exe']
        else:
            return filename in ['ffmpeg']
            
class DeforumVideoGrid:
    def __init__(self, batch_dir: str, thumbnail_size: int = 150, fps: int = 24, 
                 ffmpeg_path: Optional[str] = None, padding: int = 5):
        self.batch_dir = Path(batch_dir)
        self.thumbnail_size = thumbnail_size
        self.fps = fps
        self.padding = padding
        self.temp_dir = None
        self.ffmpeg_path = ffmpeg_path or self._locate_ffmpeg()
        
        # Text styling parameters (updated for FFmpeg 15)
        self.font_size = max(12, self.thumbnail_size // 12)
        self.text_height = self.font_size + 15
        self.param_name_height = self.font_size + 5
        self.left_margin = 100  # Increased left margin for horizontal Y-axis labels
        self.text_color = 'white'
        self.text_bg_color = 'black@0.7'
        
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg not found. Please install FFmpeg or specify path with --ffmpeg-path")
    
    def _locate_ffmpeg(self) -> Optional[str]:
        """Locate FFmpeg executable."""
        return FFmpegLocator.find_ffmpeg()
        
    def find_video_files(self) -> List[Tuple[Path, Dict]]:
        """Find all video files in batch subdirectories and extract parameter info."""
        video_files = []
        
        for subfolder in self.batch_dir.iterdir():
            if not subfolder.is_dir():
                continue
                
            # Look for video files in subfolder
            videos = list(subfolder.glob("*.mp4"))
            if not videos:
                continue
                
            # Prioritize renamed videos (folder.mp4) over timestamp videos
            renamed_video = None
            timestamp_video = None
            
            for video in videos:
                if video.stem == subfolder.name:
                    # This is a renamed video matching folder name
                    renamed_video = video
                    break
                elif re.match(r'^\d{14}$', video.stem):
                    # This is a timestamp-only video (YYYYMMDDHHMMSS pattern)
                    timestamp_video = video
            
            # Use renamed video if available, otherwise use timestamp video
            video_path = renamed_video or timestamp_video or videos[0]
            
            # Extract parameter information from folder name (not video name)
            params = self.extract_parameters_from_folder(subfolder.name)
            
            video_files.append((video_path, params))
            
        return video_files
    
    def extract_parameters_from_folder(self, folder_name: str) -> Dict:
        """Extract all parameter-value pairs from folder name using multiple strategies."""
        params = {
            'parameters': {},
            'folder_name': folder_name
        }
        
        # Remove timestamp from folder name for cleaner parameter extraction
        cleaned_name = re.sub(r'\d{14}_?', '', folder_name)
        
        # Strategy 1: Extract schedule parameters (most common in Deforum)
        schedule_pattern = r'(\w*strength_schedule)_([^_]+).*?(\w*cfg_scale_schedule)_([^_]+)'
        schedule_match = re.search(schedule_pattern, cleaned_name)
        if schedule_match:
            x_param_full, x_val, y_param_full, y_val = schedule_match.groups()
            # Extract clean parameter names
            x_param = 'strength_schedule' if 'strength_schedule' in x_param_full else x_param_full
            y_param = 'cfg_scale_schedule' if 'cfg_scale_schedule' in y_param_full else y_param_full
            params['parameters'][x_param] = self.convert_parameter_value(x_val)
            params['parameters'][y_param] = self.convert_parameter_value(y_val)
            return params
        
        # Strategy 2: General parameter_value pattern
        patterns = [
            r'(\w+_schedule)_([^_]+)',  # schedule parameters
            r'(\w+)_([^_\-]+)',         # general param_value
            r'(\w+)-([^_\-]+)',         # param-value
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, cleaned_name)
            for param, value in matches:
                # Skip numeric-only parameters (likely timestamps)
                if param.isdigit():
                    continue
                    
                # Skip common non-parameter words unless they're numeric values
                skip_words = {'seed', 'iter', 'fixed', 'random', 'date', 'settings', 'best', 'new', 'circle'}
                if param.lower() in skip_words and not self.is_numeric_value(value):
                    continue
                    
                # Try to convert value to appropriate type
                converted_value = self.convert_parameter_value(value)
                params['parameters'][param] = converted_value
        
        # Strategy 3: Extract from XYZ plot naming conventions
        xyz_patterns = [
            r'(\w+_schedule)_([^_]+)_(\w+_schedule)_([^_]+)',  # schedule_val_schedule_val
            r'(\w+)_(\w+)_([^_]+)_(\w+)_([^_]+)',              # x_param_x_val_y_param_y_val
            r'(\w+)-([^_]+)_(\w+)-([^_]+)',                    # x_param-x_val_y_param-y_val
        ]
        
        for pattern in xyz_patterns:
            match = re.search(pattern, cleaned_name)
            if match and len(match.groups()) >= 4:
                x_param, x_val, y_param, y_val = match.groups()[:4]
                params['parameters'][x_param] = self.convert_parameter_value(x_val)
                params['parameters'][y_param] = self.convert_parameter_value(y_val)
                break
        
        return params
    
    def is_numeric_value(self, value: str) -> bool:
        """Check if a string represents a numeric value."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def convert_parameter_value(self, value: str):
        """Convert string value to appropriate numeric type if possible."""
        # Try integer conversion
        try:
            if '.' not in value:
                return int(value)
        except ValueError:
            pass
        
        # Try float conversion
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string if no conversion possible
        return value
    
    def discover_parameter_space(self, video_files: List[Tuple[Path, Dict]]) -> Dict:
        """Analyze all folders to discover the complete parameter space."""
        all_parameters = {}
        parameter_frequencies = {}
        
        # Collect all parameters and their frequencies
        for _, params in video_files:
            for param_name, param_value in params['parameters'].items():
                if param_name not in all_parameters:
                    all_parameters[param_name] = set()
                    parameter_frequencies[param_name] = 0
                
                all_parameters[param_name].add(param_value)
                parameter_frequencies[param_name] += 1
        
        # Find the two most common parameters with multiple values
        valid_params = {}
        for param_name, values in all_parameters.items():
            if len(values) > 1:  # Parameter must have multiple values
                valid_params[param_name] = {
                    'values': values,
                    'frequency': parameter_frequencies[param_name],
                    'value_count': len(values)
                }
        
        # Sort by frequency and value count to find best X/Y candidates
        sorted_params = sorted(
            valid_params.items(),
            key=lambda x: (x[1]['frequency'], x[1]['value_count']),
            reverse=True
        )
        
        return {
            'all_parameters': all_parameters,
            'valid_parameters': valid_params,
            'best_candidates': sorted_params[:2] if len(sorted_params) >= 2 else sorted_params
        }
    
    def organize_grid_layout(self, video_files: List[Tuple[Path, Dict]]) -> Tuple[List[List[Path]], List[str], List[str], str, str]:
        """Organize videos into grid layout using dynamic parameter discovery."""
        if not video_files:
            return [], [], [], "", ""
        
        # Discover parameter space across all folders
        param_space = self.discover_parameter_space(video_files)
        
        # Get valid parameters
        valid_params = [name for name, data in param_space['valid_parameters'].items() if len(data['values']) > 1]
        
        if len(valid_params) >= 2:
            # Assign parameters based on Deforum conventions
            x_param_name = None
            y_param_name = None
            
            # Find strength_schedule for X-axis
            for param in valid_params:
                if 'strength_schedule' in param:
                    x_param_name = param
                    break
            
            # Find cfg_scale_schedule for Y-axis
            for param in valid_params:
                if 'cfg_scale_schedule' in param:
                    y_param_name = param
                    break
            
            # Fallback to first two parameters if specific ones not found
            if not x_param_name:
                x_param_name = valid_params[0]
            if not y_param_name:
                y_param_name = valid_params[1] if len(valid_params) > 1 else valid_params[0]
            
            print(f"Selected parameters: X='{x_param_name}', Y='{y_param_name}'")
            
            # Build grid
            x_values = sorted(param_space['all_parameters'][x_param_name], key=self.sort_key)
            y_values = sorted(param_space['all_parameters'][y_param_name], key=self.sort_key)
            
            video_dict = {}
            for video_path, params in video_files:
                folder_params = params['parameters']
                x_val = folder_params.get(x_param_name)
                y_val = folder_params.get(y_param_name)
                
                if x_val is not None and y_val is not None:
                    video_dict[(x_val, y_val)] = video_path
            
            grid = []
            for y_val in y_values:
                row = []
                for x_val in x_values:
                    video_path = video_dict.get((x_val, y_val))
                    row.append(video_path)
                grid.append(row)
            
            x_labels = [str(val) for val in x_values]
            y_labels = [str(val) for val in y_values]
            
            return grid, x_labels, y_labels, x_param_name, y_param_name
            
        elif len(valid_params) == 1:
            param_name = valid_params[0]
            param_values = sorted(param_space['all_parameters'][param_name], key=self.sort_key)
            
            row = []
            for val in param_values:
                for video_path, params in video_files:
                    if params['parameters'].get(param_name) == val:
                        row.append(video_path)
                        break
                else:
                    row.append(None)
            
            return [row], [str(val) for val in param_values], ["All Videos"], param_name, "Index"
        
        else:
            # Square grid fallback
            total_videos = len(video_files)
            grid_size = int(total_videos ** 0.5) + (1 if total_videos ** 0.5 != int(total_videos ** 0.5) else 0)
            
            grid = []
            video_index = 0
            
            for i in range(grid_size):
                row = []
                for j in range(grid_size):
                    if video_index < total_videos:
                        row.append(video_files[video_index][0])
                        video_index += 1
                    else:
                        row.append(None)
                grid.append(row)
            
            return grid, [f"Col {i+1}" for i in range(grid_size)], [f"Row {i+1}" for i in range(grid_size)], "Column", "Row"
    
    def sort_key(self, val):
        """Universal sort key function for mixed data types."""
        try:
            return (0, float(val))  # Numeric values get priority
        except (ValueError, TypeError):
            return (1, str(val))    # String values sorted separately
    
    def get_video_duration(self, video_path: Path) -> float:
        """Get video duration using FFprobe."""
        try:
            # Try ffprobe first (more reliable)
            ffprobe_path = self.ffmpeg_path.replace('ffmpeg', 'ffprobe')
            cmd = [
                ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return float(data['format']['duration'])
        except Exception:
            pass
        
        # Fallback to ffmpeg
        try:
            cmd = [
                self.ffmpeg_path,
                '-i', str(video_path),
                '-f', 'null',
                '-'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            # Parse duration from stderr output
            duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2}\.?\d*)', result.stderr)
            if duration_match:
                hours, minutes, seconds = duration_match.groups()
                return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        except Exception as e:
            print(f"Warning: Could not get duration for {video_path}: {e}")
        
        return 10.0  # Default fallback duration
    
    def create_placeholder_video(self, duration: float) -> Path:
        """Create a black placeholder video for empty grid cells."""
        placeholder_path = self.temp_dir / "placeholder.mp4"
        
        cmd = [
            self.ffmpeg_path,
            '-f', 'lavfi',
            '-i', f'color=black:size={self.thumbnail_size}x{self.thumbnail_size}:duration={duration}:rate={self.fps}',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-y',
            str(placeholder_path)
        ]
        
        subprocess.run(cmd, capture_output=True, timeout=30)
        return placeholder_path
    
    def resize_video(self, input_path: Path, output_path: Path, duration: float) -> bool:
        """Resize video to thumbnail size and ensure consistent duration."""
        cmd = [
            self.ffmpeg_path,
            '-i', str(input_path),
            '-vf', f'scale={self.thumbnail_size}:{self.thumbnail_size}:force_original_aspect_ratio=decrease,pad={self.thumbnail_size}:{self.thumbnail_size}:(ow-iw)/2:(oh-ih)/2:black',
            '-t', str(duration),
            '-r', str(self.fps),
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-y',
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    
    def calculate_grid_dimensions(self, rows: int, cols: int) -> Tuple[int, int]:
        """Calculate final grid dimensions including padding and labels."""
        # Grid content dimensions
        grid_width = cols * self.thumbnail_size + (cols - 1) * self.padding
        grid_height = rows * self.thumbnail_size + (rows - 1) * self.padding
        
        # Add space for labels with increased left margin
        top_margin = self.text_height + self.param_name_height + self.padding
        total_width = grid_width + self.left_margin
        total_height = grid_height + top_margin
        
        return total_width, total_height
    
    def create_grid_video(self, grid: List[List[Path]], output_path: Path, 
                         x_labels: List[str], y_labels: List[str],
                         x_param_name: str, y_param_name: str) -> bool:
        """Create the final grid video with padding and labels using FFmpeg."""
        if not grid:
            return False
        
        rows = len(grid)
        cols = len(grid[0])
        
        # Get maximum duration from all videos
        max_duration = 0
        for row in grid:
            for video_path in row:
                if video_path:
                    duration = self.get_video_duration(video_path)
                    max_duration = max(max_duration, duration)
        
        if max_duration == 0:
            max_duration = 10.0
        
        # Create temporary directory for resized videos
        self.temp_dir = Path(tempfile.mkdtemp())
        placeholder_path = self.create_placeholder_video(max_duration)
        
        # Resize all videos
        resized_videos = []
        for i, row in enumerate(grid):
            resized_row = []
            for j, video_path in enumerate(row):
                if video_path and video_path.exists():
                    resized_path = self.temp_dir / f"resized_{i}_{j}.mp4"
                    if self.resize_video(video_path, resized_path, max_duration):
                        resized_row.append(resized_path)
                    else:
                        resized_row.append(placeholder_path)
                else:
                    resized_row.append(placeholder_path)
            resized_videos.append(resized_row)
        
        # Calculate final dimensions
        total_width, total_height = self.calculate_grid_dimensions(rows, cols)
        
        # Build FFmpeg filter complex for grid with padding and labels
        inputs = []
        filter_parts = []
        
        # Add all input videos
        for row in resized_videos:
            for video_path in row:
                inputs.extend(['-i', str(video_path)])
        
        # Create base color canvas
        canvas_filter = f"color=black:size={total_width}x{total_height}:duration={max_duration}:rate={self.fps}[canvas]"
        filter_parts.append(canvas_filter)
        
        # Add grid videos with padding
        input_idx = 0
        current_output = "[canvas]"
        
        for i, row in enumerate(resized_videos):
            for j, _ in enumerate(row):
                # Calculate position with updated left margin
                x_pos = self.left_margin + j * (self.thumbnail_size + self.padding)
                y_pos = self.text_height + self.param_name_height + self.padding + i * (self.thumbnail_size + self.padding)
                
                next_output = f"[overlay_{i}_{j}]"
                overlay_filter = f"{current_output}[{input_idx}:v]overlay={x_pos}:{y_pos}{next_output}"
                filter_parts.append(overlay_filter)
                current_output = next_output
                input_idx += 1
        
        # Rename final overlay output for text processing
        if current_output != "[canvas]":
            # Use the final overlay output directly, no need for null filter
            grid_output = current_output
        else:
            grid_output = current_output
        
        # Add text labels
        text_filters = []
        
        # Add X-axis value labels (below parameter name)
        for j, label in enumerate(x_labels):
            x_pos = self.left_margin + j * (self.thumbnail_size + self.padding) + self.thumbnail_size // 2
            y_pos = self.text_height + 5
            text_filter = f"drawtext=text='{label}':fontsize={self.font_size}:fontcolor={self.text_color}:box=1:boxcolor={self.text_bg_color}:x={x_pos}-text_w/2:y={y_pos}"
            text_filters.append(text_filter)
        
        # Add Y-axis value labels (horizontal on left with increased margin)
        for i, label in enumerate(y_labels):
            x_pos = 50  # Positioned in the left margin
            y_pos = self.text_height + self.param_name_height + self.padding + i * (self.thumbnail_size + self.padding) + self.thumbnail_size // 2
            text_filter = f"drawtext=text='{label}':fontsize={self.font_size}:fontcolor={self.text_color}:box=1:boxcolor={self.text_bg_color}:x={x_pos}:y={y_pos}-text_h/2"
            text_filters.append(text_filter)
        
        # Add X parameter name at top center
        if x_param_name:
            x_param_x = total_width // 2
            x_param_y = 5
            x_param_filter = f"drawtext=text='{x_param_name}':fontsize={self.font_size + 2}:fontcolor={self.text_color}:box=1:boxcolor={self.text_bg_color}:x={x_param_x}-text_w/2:y={x_param_y}"
            text_filters.append(x_param_filter)
        
        # Add Y parameter name horizontally on left side
        if y_param_name and rows > 1:
            y_param_x = 5
            y_param_y = total_height // 2 - self.font_size
            y_param_filter = f"drawtext=text='{y_param_name}':fontsize={self.font_size + 2}:fontcolor={self.text_color}:box=1:boxcolor={self.text_bg_color}:x={y_param_x}:y={y_param_y}"
            text_filters.append(y_param_filter)
        
        # Combine all text filters
        if text_filters:
            final_filter = f"{grid_output}{','.join(text_filters)}[final]"
            filter_parts.append(final_filter)
            output_mapping = "[final]"
        else:
            output_mapping = grid_output
        
        # Build complete FFmpeg command
        cmd = [self.ffmpeg_path] + inputs + [
            '-filter_complex', ';'.join(filter_parts),
            '-map', f'{output_mapping}',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-r', str(self.fps),
            '-y',
            str(output_path)
        ]
        
        print(f"Creating grid video: {output_path}")
        print(f"Grid layout: {rows}x{cols}")
        print(f"Duration: {max_duration:.2f}s")
        print(f"Final dimensions: {total_width}x{total_height}")
        print(f"Parameters: X={x_param_name}, Y={y_param_name}")
        print(f"Using FFmpeg: {self.ffmpeg_path}")
        
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr.decode()}")
        
        # Cleanup temporary files
        import shutil
        shutil.rmtree(self.temp_dir)
        
        return result.returncode == 0
    
    def generate_grid(self, output_path: Optional[str] = None) -> bool:
        """Main method to generate video grid."""
        if not self.batch_dir.exists():
            print(f"Error: Batch directory {self.batch_dir} does not exist")
            return False
        
        # Find video files
        print(f"Scanning {self.batch_dir} for video files...")
        video_files = self.find_video_files()
        
        if not video_files:
            print("No video files found in batch subdirectories")
            return False
        
        print(f"Found {len(video_files)} video files")
        
        # Organize grid layout
        grid, x_labels, y_labels, x_param_name, y_param_name = self.organize_grid_layout(video_files)
        
        if not grid:
            print("Could not organize videos into grid")
            return False
        
        # Generate output filename if not provided
        if not output_path:
            batch_name = self.batch_dir.name
            output_path = self.batch_dir / f"{batch_name}_grid.mp4"
        else:
            output_path = Path(output_path)
        
        # Create grid video
        success = self.create_grid_video(grid, output_path, x_labels, y_labels, x_param_name, y_param_name)
        
        if success:
            print(f"Grid video created successfully: {output_path}")
            return True
        else:
            print("Failed to create grid video")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Generate video grids from Deforum batch outputs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deforum_video_grid.py batch_folder
  python deforum_video_grid.py batch_folder -o output_grid.mp4 -s 200 -f 30
  python deforum_video_grid.py "D:/outputs/batch_20231201" --size 150 --padding 10
        """
    )
    
    parser.add_argument(
        'batch_directory',
        help='Directory containing Deforum batch output folders'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output video file path (default: auto-generated)'
    )
    
    parser.add_argument(
        '-s', '--size',
        type=int,
        default=150,
        help='Thumbnail size in pixels (default: 150)'
    )
    
    parser.add_argument(
        '-f', '--fps',
        type=int,
        default=24,
        help='Output video frame rate (default: 24)'
    )
    
    parser.add_argument(
        '-p', '--padding',
        type=int,
        default=5,
        help='Padding between videos in pixels (default: 5)'
    )
    
    parser.add_argument(
        '--ffmpeg-path',
        help='Custom path to FFmpeg executable'
    )
    
    args = parser.parse_args()
    
    # Create grid generator
    generator = DeforumVideoGrid(
        batch_dir=args.batch_directory,
        thumbnail_size=args.size,
        fps=args.fps,
        ffmpeg_path=args.ffmpeg_path,
        padding=args.padding
    )
    
    # Generate grid
    success = generator.generate_grid(args.output)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())