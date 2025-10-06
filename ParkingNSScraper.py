import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_for_plate(plate_number):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://portal.parkingns.rs/ppk")
    time.sleep(3)

    input_field = driver.find_element(By.ID, "platePr")
    input_field.send_keys(plate_number)

    check_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Провера')]")
    check_button.click()
    time.sleep(5)

    try:
        card_text_element = driver.find_element(By.CLASS_NAME, "card-text-lg")
        card_text = "NONE"
    except Exception as e:
        card_text = None
    if card_text is None:
        try:
            order_number_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Број налога')]")
            if len(order_number_elements) > 0:
                #for nalog in order_number_elements:
                #   print(nalog.text)
                card_text = "You currently have " +str(len(order_number_elements))+ " tikets for parking in Novi Sad."
        except Exception as e:
            card_text = "No result or error"

    driver.quit()

    return card_text


def process_csv(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)

        results = []

        for row in csv_reader:
            plate_number = row[0]  
            print(f"Processing plate: {plate_number}")
            result = scrape_for_plate(plate_number)
            results.append([plate_number, result])

    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["Plate Number", "Result"])
        csv_writer.writerows(results)


input_csv = 'plate_numbers.csv'  
output_csv = 'scraped_results.csv' 
process_csv(input_csv, output_csv)

print("Scraping complete. Results saved to 'scraped_results.csv'.")
