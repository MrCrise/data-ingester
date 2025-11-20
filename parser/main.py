from database import save_to_db, count_cases, clear_all_tables
from parser import parse_data, create_chrome_driver, create_firefox_driver


if __name__ == '__main__':  
    try:
        driver = create_chrome_driver()
        
        parsed_cases, parsed_documents = parse_data(driver, start_page = 3)
        save_to_db(parsed_cases, parsed_documents)
        print(count_cases())
    finally:
        driver.quit()