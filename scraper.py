"""
This script performs web scraping on the Función Judicial website of Ecuador to retrieve legal case data.
The script uses Selenium WebDriver and BeautifulSoup to automate navigation through the website and extract data.
The extracted data is then formatted into JSON and sent to a local API endpoint using the requests library.
"""

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json


def get_any_table_html(x_path):
    """
    Retrieves the HTML table element located at the specified XPath and returns it as a BeautifulSoup object.

    :param x_path: str - The XPath of the table element to retrieve.
    :return: BeautifulSoup - A BeautifulSoup object representing the retrieved HTML table.
    """
    table = driver.find_element(By.XPATH, x_path)
    html_table = table.get_attribute('innerHTML')
    return BeautifulSoup(html_table, 'html.parser')


def get_details_data():
    """
    Retrieves the details of a legal case and returns them as a dictionary.

    :return: dict - A dictionary containing the details of a legal case.
    """
    # Will be used to change default names to Json like format
    table_names = {
        'No. proceso:': 'process_num',
        'No. de ingreso:': 'entry_number',
        'Dependencia jurisdiccional:': 'jurisdictional_unit',
        'Acción/Infracción:': 'action',
        'Actor(es)/Ofendido(s):': 'actors',
        'Demandado(s)/Procesado(s):': 'defendant'
    }

    details_table_soup = get_any_table_html(
        '//*[@id="formJuicioDetalle:j_idt73"]')
    table_rows = details_table_soup.find_all('tr')

    details = {}
    for row in table_rows:
        cols = row.find_all('td')
        for i in range(0, len(cols), 2):
            key_name = table_names.get(cols[i].text, None)
            if key_name:
                details[key_name] = cols[i + 1].text

    return details


def get_legal_proceedings():
    """
    Retrieves the legal proceedings of a legal case and returns them as a list of dictionaries.

    :return: list - A list containing the legal proceedings of a legal case.
    """
    details_table_soup = get_any_table_html(
        '//*[@id="formJuicioDetalle:dataTable"]/div/table')
    table_rows = details_table_soup.find_all('tr')

    proceedings = []
    for row in table_rows:
        cols = row.find_all(attrs={"role": "gridcell"})
        proceeding = {}
        for i in range(0, len(cols), 2):
            proceeding['date'] = cols[i].text

            col2 = cols[i + 1]
            title = col2.find('legend') and col2.find('legend').text
            content = col2.find(
                class_='ui-fieldset-content') and col2.find(class_='ui-fieldset-content').text
            proceeding['title'] = title
            # Replace quote to avoid error when sending data to API
            proceeding['content'] = content.replace('"', "'")

        if proceeding:
            proceedings.append(proceeding)

    return proceedings


def go_to_legal_proceedings():
    """
    Scrapes the legal proceedings data of a case and sends a POST request to a specified URL.
    """

    # Get the HTML of the table that contains the proceedings data.
    proceedings_table_soup = get_any_table_html(
        '//*[@id="formJuicioDialogo:dataTableMovimiento_data"]')
    table_rows = proceedings_table_soup.find_all('tr')

    # Remove unnecessary first row.
    table_rows.pop(0)

    # Iterate through the rows and click the details button for each row.
    for row in table_rows:
        last_column = row.contents[-1]

        # Find the details button ID.
        details_button = last_column.find('button')
        details_button_id = details_button and details_button.get('id')

        # If the details button ID is found, click it and scrape the proceedings data.
        if details_button_id:
            driver.find_element(By.ID, details_button_id).click()
            time.sleep(3)

            process_detail = get_details_data()
            proceedings = get_legal_proceedings()

            process_detail['legal_proceedings'] = proceedings

            # Send a POST request to create a new record.
            res = requests.post(
                url='http://127.0.0.1:8000/create-process/', json=process_detail)
            print('New record created' if res.status_code ==
                  200 else 'Something went wrong')

            # Click the "close" button to close the proceedings details window.
            driver.find_element(By.NAME, 'formJuicioDetalle:btnCerrar').click()
            time.sleep(1)


def go_to_details():
    """
    Scrapes the details of all cases in the search results.
    """

    # Get the HTML of the table that contains the case details.
    registers_table_soup = get_any_table_html(
        '//*[@id="form1:dataTableJuicios2_data"]')
    table_rows = registers_table_soup.find_all('tr')

    # Iterate through the rows and click the details button for each row.
    for row in table_rows:

        last_column = row.contents[-1]

        # Find the details button ID.
        details_button = last_column.find('button')
        details_button_id = details_button and details_button.get('id')

        # If the details button ID is found, click it and scrape the legal proceedings data.
        if details_button_id:
            driver.find_element(By.ID, details_button_id).click()
            time.sleep(2)
            go_to_legal_proceedings()

            # Click the "cancel" button to return to the search results.
            driver.find_element(
                By.NAME, 'formJuicioDialogo:btnCancelar').click()


def start_searching(search_id):
    """
    Enters the search ID and clicks the search button.
    """

    plaintiff_id = driver.find_element(
        By.XPATH, '//*[@id="form1:txtActorCedula"]')
    plaintiff_id.send_keys(search_id)

    search_button = driver.find_element(
        By.XPATH, '//*[@id="form1:butBuscarJuicios"]')
    search_button.click()
    time.sleep(3)


if __name__ == '__main__':
    """
    Main program that runs the web scraper.
    """

    # Initialize the Chrome driver.
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.get(
        'http://consultas.funcionjudicial.gob.ec/informacionjudicial/public/informacion.jsf')

    start_searching('0968599020001')  # Search id hardcoded for simplicity
    go_to_details()

    print('The scraper has finished its job!')
