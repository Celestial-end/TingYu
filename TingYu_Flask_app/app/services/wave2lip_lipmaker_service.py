import time
from sync import Sync
from sync.common import Audio, GenerationOptions, Video
from sync.core.api_error import ApiError
from app.config import Config_Cloud
from app.utils import file_utils



def video_generate(video_name,audio_name):
        
# ---------- UPDATE API KEY ----------
# Replace with your Sync.so API key
    api_key = Config_Cloud.SYNC_API_KEY

# ----------[OPTIONAL] UPDATE INPUT VIDEO AND AUDIO URL ----------
# URL to your source video
    if file_utils.validate_video_content(video_name) == False:
        return "Invalid video file"
    else:
        video_url = file_utils.generate_unique_filename(video_name)
# URL to your audio file
    if file_utils.validate_audio_file(audio_name) == False:
        return "Invalid audio file"
    else:
        audio_url = file_utils.generate_unique_filename(audio_name)
# ----------------------------------------

    client = Sync(
        base_url="https://api.sync.so", 
        api_key=api_key
    ).generations

    print("Starting lip sync generation job...")

    try:
        response = client.create(
        input=[Video(url=video_url),Audio(url=audio_url)],
        model="lipsync-2",
        options=GenerationOptions(sync_mode="loop"),
            #outputFileName="quickstart"
        )
    except ApiError as e:
        print(f'create generation request failed with status code {e.status_code} and error {e.body}')
        exit()

    job_id = response.id
    print(f"Generation submitted successfully, job id: {job_id}")

    generation = client.get(job_id)
    status = generation.status
    while status not in ['COMPLETED', 'FAILED']:
        print('polling status for generation', job_id)
        time.sleep(10)
        generation = client.get(job_id)
        status = generation.status
        print('current status:', status)

    output_url = generation.output_url
    if status == 'COMPLETED':
        print('generation', job_id, 'completed successfully, output url:', generation.output_url)
    else:
        print('generation', job_id, 'failed')

    return output_url
