import pyautogui
import time
from PIL import Image
from datetime import datetime
from robot.libraries.BuiltIn import BuiltIn

class DesktopKeywords:
    def image_based_mouseclick(self,picture, button: str, click: int,current_scale,target_scale, confidence: float = 0.7):
        try:
            time.sleep(1)
            print("---->", picture)
            r = None
            print("r value after", r)

            rescaled_image = self.scale_image(picture, current_scale, target_scale)
            rescaled_img_path = 'rescaled_img_temp.png'
            rescaled_image.save(rescaled_img_path)
            # rescaled_image = self.scale_image(picture, current_scale, target_scale)
            counter = 0
            while counter < 20:
                try:
                    print("----> inside try block")
                    r = pyautogui.locateCenterOnScreen(rescaled_img_path, grayscale=True, confidence=confidence)
                    print("r value:")
                    print("=> {}".format(r))
                    if r is not None:
                        print("Trying to click on:", r)
                        pyautogui.moveTo(r[0], r[1], 0.2)
                        pyautogui.click(button=button, clicks=int(click), interval=0.25)
                        return True
                except:
                    pass
                counter += 1
                time.sleep(0.5)
            return False
        except Exception as e:
            print(f"Error in locate_and_click: {e}")
            return False

    def launch_application(self,app_name, delay=1):

        try:
            pyautogui.hotkey('win', 'r')  # Open Run dialog
            time.sleep(delay)

            pyautogui.typewrite(app_name)  # Type app name or path
            time.sleep(0.5)

            pyautogui.press('enter')  # Launch app
            time.sleep(delay)

            return True
        except Exception as e:
            print(f"Error launching {app_name}: {e}")
            return False

    def send_text(self,text, interval=0.05):

        try:
            pyautogui.typewrite(text, interval=interval)
            return True
        except Exception as e:
            print(f"Error sending text: {e}")
            return False

    def scale_image(self,image_path, current_scale_percent, target_scale_percent):
        print("imagepath",image_path)
        image = Image.open(image_path)
        print("image",image)
        scaling_factor = float(target_scale_percent) / float(current_scale_percent)
        print("Scaling factor--->", scaling_factor)

        original_width, original_height = image.size
        new_width = round(original_width * scaling_factor)
        new_height = round(original_height * scaling_factor)

        if scaling_factor < 1:
            resample_filter = Image.Resampling.LANCZOS
        else:
            resample_filter = Image.Resampling.BICUBIC

        resized_image = image.resize((new_width, new_height), resample_filter)
        return resized_image


    def check_log_entries(seld,start_time, check_log, file_path):
        initial_time = datetime.strptime(start_time, "%d-%m-%Y %H:%M:%S")
        BuiltIn().log_to_console(f"\nProvided inputs: {initial_time}, {file_path}, {check_log}")

        with open(file_path) as f:
            data = f.readlines()

            for num, line in enumerate(data):
                log_time = line[0:19]
                try:
                    logs_time = datetime.strptime(log_time, "%d-%m-%Y %H:%M:%S")
                    if (logs_time - initial_time).total_seconds() >= 0.0:
                        for sub_line in data[num:num + 150]:
                            print("subline-->", sub_line)
                            if check_log in sub_line:
                                print("the log found,", check_log)
                                BuiltIn().log_to_console(f"Found log entry: {check_log}")
                                return 'True'
                except ValueError:
                    pass
        return 'False'


    def clear_log_file(self,file_path):
        try:
            with open(file_path, 'w') as file:
                file.truncate(0)
            print(f"Log file '{file_path}' has been cleared.")
        except Exception as e:
            print(f"Error clearing log file: {e}")
