import tempfile
import os
import ffmpeg
from fastapi import HTTPException

class AudioProcessor:
    @staticmethod
    def convert_to_wav(input_path: str, sample_rate: int = 16000, channels: int = 1) -> str:
        """将音频文件转换为WAV格式
        
        Args:
            input_path: 输入音频文件路径
            sample_rate: 输出采样率，默认为16000Hz
            channels: 输出声道数，默认为1（单声道）
            
        Returns:
            转换后的WAV文件路径
            
        Raises:
            HTTPException: 转换失败时抛出
        """
        output_path = tempfile.mktemp(suffix=".wav")
        
        try:
            # 使用ffmpeg进行格式转换
            (ffmpeg
             .input(input_path)
             .output(output_path, ac=channels, ar=sample_rate, format='wav')
             .overwrite_output()
             .run(capture_stdout=True, capture_stderr=True))
            
            return output_path
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            raise HTTPException(status_code=500, detail="Audio conversion failed")
        except Exception as e:
            print(f"Audio conversion error: {e}")
            raise HTTPException(status_code=500, detail=f"Audio conversion failed: {str(e)}")
    
    @staticmethod
    def cleanup_temp_files(file_paths: list):
        """清理临时文件
        
        Args:
            file_paths: 要清理的文件路径列表
        """
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                    print(f"Cleaned up temp file: {file_path}")
                except Exception as e:
                    print(f"Failed to cleanup temp file {file_path}: {e}")