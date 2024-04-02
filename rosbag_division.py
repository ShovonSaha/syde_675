import rosbag
import os
from datetime import datetime
import glob

def segment_rosbag(original_bag_path, cutoff_time, before_bag_path, after_bag_path):
    """
    Segments a ROS bag into two parts based on a specified cutoff time.
    """
    print("Opening original rosbag:", original_bag_path)
    with rosbag.Bag(original_bag_path, 'r') as original_bag:
        start_time = original_bag.get_start_time()
        cutoff_time_rospy = start_time + cutoff_time
        print(f"Segmenting rosbag at {datetime.utcfromtimestamp(cutoff_time_rospy).strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
        
        with rosbag.Bag(before_bag_path, 'w') as before_bag, rosbag.Bag(after_bag_path, 'w') as after_bag:
            for topic, msg, t in original_bag.read_messages():
                if t.to_sec() <= cutoff_time_rospy:
                    before_bag.write(topic, msg, t)
                else:
                    after_bag.write(topic, msg, t)
                    
    print("Segmentation completed.")
    print("Before cutoff rosbag saved to:", before_bag_path)
    print("After cutoff rosbag saved to:", after_bag_path)

def process_directory(directory_path, cutoff_time):
    """
    Processes all rosbag files in the specified directory, segmenting each based on the cutoff time.
    """
    # Ensure path is absolute
    directory_path = os.path.expanduser(directory_path)
    bag_files = glob.glob(os.path.join(directory_path, '*.bag'))
    
    for bag_file in bag_files:
        base_name = os.path.splitext(os.path.basename(bag_file))[0]
        before_bag_path = os.path.join(directory_path, f"{base_name}_before.bag")
        after_bag_path = os.path.join(directory_path, f"{base_name}_after.bag")
        segment_rosbag(bag_file, cutoff_time, before_bag_path, after_bag_path)

# Example usage
directory_path = '~/SYDE675_project/syde_675_data/approach_data'
cutoff_time = 13  # Adjust this cutoff time as needed for your scenario

process_directory(directory_path, cutoff_time)