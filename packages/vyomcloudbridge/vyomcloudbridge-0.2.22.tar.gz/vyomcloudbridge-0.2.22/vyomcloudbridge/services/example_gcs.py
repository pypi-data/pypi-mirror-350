# vyomcloudbridge/queue_writer_json.py
import time
from vyomcloudbridge.utils.common import generate_unique_id


def main():
    # Example 1
    from vyomcloudbridge.services.queue_writer_json import QueueWriterJson

    try:
        writer = QueueWriterJson()
        message_data = {"lat": 75.66666, "long": 73.0589455}
        data_source = "MACHINE_POSE"  # event, warning, camera1, camera2,
        data_type = "json"  # image, binary, json
        mission_id = "111333"

        epoch_ms = int(time.time() * 1000)
        uuid_padding = generate_unique_id(4)
        filename = f"{epoch_ms}_{uuid_padding}.json"

        writer.write_message(
            message_data=message_data,  # json or binary data
            filename=filename,  # 293749834.json, 93484934.jpg
            data_source=data_source,  # machine_pose camera1, machine_state
            data_type=data_type,  # json, binary, ros
            mission_id=mission_id,  # mission_id
            priority=1,  # 1
            destination_ids=["gcs"],  # ["s3"]
        )
    except Exception as e:
        print(f"Error writing test messages: {e}")
    finally:
        writer.cleanup()


if __name__ == "__main__":
    main()
