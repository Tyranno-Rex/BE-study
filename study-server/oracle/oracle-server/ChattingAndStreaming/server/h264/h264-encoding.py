import ffmpeg
import os
input_file = 'C:/Users/admin/project/oracle/oracle-server/h264/input.mp4'
output_file = 'C:/Users/admin/project/oracle/oracle-server/h264/output.mp4'

# # H.264로 압축
ffmpeg.input(input_file).output(output_file, vcodec='libx264').run()


print(os.path.getsize(input_file))
print(os.path.getsize(output_file))