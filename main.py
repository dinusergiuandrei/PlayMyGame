from data_collector import collect_data
from move_maker import train_and_save_model, play

if __name__ == '__main__':
    # probably better to run only one at a time from next 3 lines.
    collect_data(total_frames=1000, buffer_size=1000, rate=40)
    train_and_save_model()
    play()
