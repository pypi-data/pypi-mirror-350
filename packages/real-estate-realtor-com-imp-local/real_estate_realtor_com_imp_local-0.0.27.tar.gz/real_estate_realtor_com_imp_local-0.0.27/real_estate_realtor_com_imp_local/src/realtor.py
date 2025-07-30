import os
import json
import re

import mysql.connector
from database_mysql_local.generic_crud import GenericCRUD

# from data_source_local.data_source_enum import DataSource
# from entity_type_local.entities_type import EntitiesType
# from entity_type_local.entity_enum import EntityTypeId
from importer_local.ImportersLocal import ImportersLocal
# from user_external_local import UserExternalsLocal
from user_external_local.user_externals_local import UserExternalsLocal
from location_local.country import Country
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from python_sdk_remote.utilities import our_get_env
import selenium

# TODO: move to const
BASE_URL = "https://www.realtor.com/international/"
PAGE_LIMIT = 5
LISTINGS_LIMIT_PER_PAGE = 6  # TODO: Why?
REAL_ESTATE_ENTITY_ID = 1
REAL_ESTATE_ENTITY_TYPE_ID = 79  # # TODO use entity_type package
REAL_ESTATE_DATA_SOURCE_ID = 15

REAL_ESTATE_REALTOR_COM_SELENIUM_IMP_COMPONENT_ID = 146
REAL_ESTATE_REALTOR_COM_SELENIUM_IMP_COMPONENT_NAME = (
    "real-estate-realtor_com-selenium-imp-local-python-package"
)
GET_LISTING_LINKS_FROM_LOCATION_FUNCTION_NAME = "real-estate-realtor_com-selenium-imp-local-python-package/realtor.py get_listing_links_from_location()"  # noqa

logger_code_init = {
    "component_id": REAL_ESTATE_REALTOR_COM_SELENIUM_IMP_COMPONENT_ID,
    "component_name": REAL_ESTATE_REALTOR_COM_SELENIUM_IMP_COMPONENT_NAME,
    "component_category": LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "tal@circlez.ai",
}

importers_local = ImportersLocal()
user_externals = UserExternalsLocal()


class Realtor(GenericCRUD, metaclass=MetaLogger, object=logger_code_init):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(
            default_schema_name="marketplace_goods_real_estate",
            default_table_name="real_estate_listing_table",
            default_view_table_name="real_estate_listing_view",
            default_column_name="real_estate_listing_id",
            is_test_data=is_test_data,
        )
        self.country = Country(is_test_data=is_test_data)
        self.REALTOR_COM_USER_EXTERNAL_ID = Realtor.create_realtor_com_user_external()

        # create a new ChromeDriver instance
        options = webdriver.ChromeOptions()
        if not our_get_env("DISABLE_HEADLESS_MODE", raise_if_not_found=False):
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def get_listing_links_from_location(self, location: str) -> list[str]:

        location_base_url = self.get_link_from_location(location)
        listings = [
            self.extract_listings_from_listings_page(f"{location_base_url}/p{page_num}")
            for page_num in range(1, PAGE_LIMIT + 1)
        ]
        listings = [item for sublist in listings for item in sublist]
        return listings

    def extract_listings_from_listings_page(self, url: str) -> list[str]:
        self.driver.get(url)
        WebDriverWait(self.driver, 5).until(
            lambda driver: self.driver.find_element(
                By.CLASS_NAME, "listing-split-view-wrapper"
            )
        )
        ul_elements = self.driver.find_elements(
            By.CLASS_NAME, "listing-split-view-wrapper"
        )
        links = [
            elem.find_element(By.TAG_NAME, "a").get_attribute("href")
            for elem in ul_elements
        ]
        # ul_next_page_elements = driver.find_elements(By.CLASS_NAME, "pagination-box")
        # li_next_page_element = ul_next_page_elements.find_element(By.TAG_NAME,"a").get_attribute('href')
        links_for_viewer = links[:LISTINGS_LIMIT_PER_PAGE]
        return links_for_viewer

    def insert_to_table(
        self, curr_location_listings_data_dict: list[dict], location: str
    ) -> None:
        country_name = self.country.get_country_name(location)
        # TODO replace with a call to location Class location-local-python-package
        location_id = super().select_one_value_by_column_and_value(
            select_clause_value="location_id",
            schema_name="location",
            view_table_name="location_general_view",
            column_name="country_name",
            column_value=country_name,
        )
        # TODO If we get exception of duplicate, maybe we should update the the tables as the real-estate listing was updated in realtor.com

        importers_data_dict = {
            "data_source_instance_id": REAL_ESTATE_DATA_SOURCE_ID,
            "data_source_type_id": REAL_ESTATE_DATA_SOURCE_ID,
            "location_id": location_id,
            "entity_type_id": REAL_ESTATE_ENTITY_TYPE_ID,
            "url": BASE_URL,
            "entity_id": REAL_ESTATE_ENTITY_ID,
            "user_external_id": self.REALTOR_COM_USER_EXTERNAL_ID,
        }
        importer_id = None
        # TODO use data_source and entity_id packages const / enum
        # TODO Can we switch to a generic insert() method and use importers_data_dict
        try:
            # importers_local.insert(
            #     data_source_instance_id=REAL_ESTATE_DATA_SOURCE_ID,
            #     data_source_type_id=REAL_ESTATE_DATA_SOURCE_ID,
            #     location_id=location_id,
            #     entity_type_id=REAL_ESTATE_ENTITY_TYPE_ID,
            #     url=BASE_URL,
            #     entity_id=REAL_ESTATE_ENTITY_ID,
            #     user_external_id=REALTOR_COM_USER_EXTERNAL_ID,
            # )
            importer_id = importers_local.insert(**importers_data_dict)
        except mysql.connector.errors.IntegrityError as e:
            self.logger.error(
                log_message="Foreign key constraint failed",
                object={
                    "data_dict": importers_data_dict,
                    "error": str(e),
                },
            )
            # Handle the specific error code for foreign key constraint
            if "1216" in str(e) or "a foreign key constraint fails" in str(e):
                self.logger.error(
                    "Foreign key constraint failed - check that referenced values exist. Maybe realtor external_user is missing.",
                    object={"exception": str(e)}
                )
            else:
                self.logger.error(
                    "Duplicate key has detected",
                    object={"exception": str(e)}
                )
        except Exception as exception:
            self.logger.exception(object={"exception": exception})
            raise exception

        try:
            # remove all rows with agent_office_phone missing values
            # curr_location_listings = curr_location_listings.dropna(subset=['agent_office_phone'])
            inserted_ids = self.insert_many_dicts(data_dicts=curr_location_listings_data_dict)
        except Exception as exception:
            self.logger.error(
                    log_message="IntegrityError",
                    object={
                        "data_dict": curr_location_listings_data_dict,
                        "error": str(exception),
                    },
                )
            if mysql.connector.errors.IntegrityError:
                self.logger.error(
                    "Duplicate key has detected", object={"exception": exception}
                )
            else:
                self.logger.exception(object={"excpetion": exception})
                raise exception

        return importer_id, inserted_ids

        # TODO
        # # Specify the table name
        # table_name = 'listings'
        # # Insert the row into the table
        # line.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        # engine.dispose()
        # with engine.connect() as conn:
        #     conn.execute(text("SELECT * FROM users")

        # new_row = {'importer_id': importer_id_int, 'agent_name': agent_name, 'agent_office_phone': phone_int,
        #            'price': price_int, 'property_type': property_type, 'land_size': land_int,
        #            'building_size': building_size_int, 'num_of_bedrooms': num_bedrooms,
        #            'num_of_bathrooms': num_bathrooms}

    def wrapper_extract_data(self, links: list[str]) -> list[dict]:
        data = [self.extract_data(link) for link in links]
        return data

    def extract_data(self, link: str) -> dict:
        # TODO: break to multiple functions
        agent_office_phone = None
        price = None
        property_type = None
        land_size = None
        building_size = None
        num_of_bedrooms = None
        num_of_bathrooms = None
        real_estate_listing_id = None
        agent_name = None

        try:
            self.driver.get(link)
            WebDriverWait(self.driver, 5).until(
                lambda driver: self.driver.find_element(By.CLASS_NAME, "listing-id")
            )
        except selenium.common.exceptions.TimeoutException as exception:
            self.logger.warning(
                f"Link was not found, exception:{exception}", object={"link": link}
            )

        title = self.driver.title
        url = self.driver.current_url
        try:
            address = re.search(r"(\w+(?:-\w+)? (?:\w+,? )+\d+)", title)
            if address:
                address = address.group(0)
                self.logger.info(object={"address": address})
        except NoSuchElementException:
            self.logger.warning(
                "No address id found", object={"title": title, "url": url}
            )
        try:
            listing_id_element = self.driver.find_element(By.CLASS_NAME, "listing-id")

            # text = 'Property ID: 9456229688'
            listing_id_element_text = listing_id_element.text
            match = re.search(r"\d+", listing_id_element_text)

            if match:
                real_estate_listing_id = int(match.group(0))
            else:
                real_estate_listing_id = None
                self.logger.warning(
                    "No listing id found", object={"title": title, "url": url}
                )
            # real_estate_listing_id = int(listing_id_element.text)

        except NoSuchElementException:
            self.logger.warning(
                "No listing id found", object={"title": title, "url": url}
            )
        try:
            agent_name_element = self.driver.find_element(By.CLASS_NAME, "agent-name")
            agent_name = agent_name_element.text
            # print(agent_name)
        except NoSuchElementException:
            self.logger.warning(
                "No agent name found", object={"title": title, "url": url}
            )
        try:
            agent_office_phone_element = self.driver.find_element(
                By.CLASS_NAME, "agent-officephone"
            )
            agent_office_phone = agent_office_phone_element.get_attribute("href")
            agent_office_phone = int("".join(re.findall(r"\d+", agent_office_phone)))
            self.logger.info(object={"agent_office_phone": agent_office_phone})
        except NoSuchElementException:
            self.logger.warning(
                "No agent office phone found", object={"title": title, "url": url}
            )
        try:
            price_element = self.driver.find_element(By.CLASS_NAME, "property-price")
            price = int("".join(re.findall(r"\d+", price_element.text)))
            self.logger.info(object={"price": price})
        except NoSuchElementException:
            self.logger.warning(
                "No property price found", object={"title": title, "url": url}
            )
        try:
            property_type_element = self.driver.find_element(
                By.CSS_SELECTOR, value=".propertyTypes .basicInfoValue"
            )

            property_type = property_type_element.text
        except NoSuchElementException:
            self.logger.warning(
                "No property type found", object={"title": title, "url": url}
            )
        try:  # TODO: use selenium.By
            land_size_element = self.driver.find_element(
                By.CSS_SELECTOR, value=".landSize .basicInfoValue span"
            )
            building_size_until_point = re.search(
                r"\d[\d,.]*(?=\.)", land_size_element.text
            ).group(0)
            land_size = int("".join(re.findall(r"\d+", building_size_until_point)))
            self.logger.info(object={"land_size": land_size})
        except NoSuchElementException:
            self.logger.warning(
                "No land size found", object={"title": title, "url": url}
            )
        try:
            building_size_element = self.driver.find_element(
                by="xpath",
                value="//div[text()='Building Size']/following-sibling::div/span",
            )
            building_size_until_point = re.search(
                r"\d[\d,.]*(?=\.)", building_size_element.text
            ).group(0)
            building_size = int("".join(re.findall(r"\d+", building_size_until_point)))
            self.logger.info(object={"building_size": building_size})
        except NoSuchElementException:
            self.logger.warning(
                "No building size found", object={"title": title, "url": url}
            )
        try:
            rooms_element = self.driver.find_element(
                By.CSS_SELECTOR, value=".rooms .basicInfoValue"
            )
            rooms = rooms_element.text
            rooms_list = rooms.split(",")
            num_of_bedrooms = num_of_bathrooms = 0
            for room in rooms_list:
                room_type = re.findall(r"[a-z]+", room)[0]
                if room_type.startswith("bath"):
                    num_of_bathrooms = int(re.findall(r"\d+", room)[0])
                elif room_type.startswith("bed"):
                    num_of_bedrooms = int(re.findall(r"\d+", room)[0])
                elif room_type.startswith("other"):
                    num_of_bedrooms = int(re.findall(r"\d+", room)[0])
                else:
                    self.logger.info(f"ignored room type: {room_type}", object={"room": room})
                    # raise Exception("you didn't prepared well")
        except NoSuchElementException:
            self.logger.warning("No rooms found", object={"title": title, "url": url})
        self.logger.info(
            "Listing Details",
            object={
                "id": real_estate_listing_id,
                "agent": {"name": agent_name, "phone": agent_office_phone},
                "property": {
                    "price": price,
                    "type": property_type,
                    "dimensions": {
                        "land_size": land_size,
                        "building_size": building_size,
                    },
                    "rooms": {
                        "bedrooms": num_of_bedrooms,
                        "bathrooms": num_of_bathrooms,
                    },
                },
            },
        )
        new_row = {
            "agent_name": agent_name,
            "agent_office_phone": agent_office_phone,
            "price": price,
            "property_type": property_type,
            "land_size": land_size,
            "building_size": building_size,
            "num_of_bedrooms": num_of_bedrooms,
            "num_of_bathrooms": num_of_bathrooms,
        }
        return new_row

    @staticmethod
    def read_locations_list_str_from_json():
        suffix = "locations.json"
        locations_file = os.path.join(os.path.dirname(__file__), suffix)
        with open(locations_file) as f:
            locations = json.load(f)
        locations_read = locations["locations"]
        return locations_read

    @staticmethod
    def get_link_from_location(location: str) -> str:
        link = BASE_URL + location
        return link

    @staticmethod
    def create_realtor_com_user_external() -> int:
        user_external_id = user_externals.insert_or_update_user_external_access_token(
            username=None,
            # TODO get the profile_id from UserContext
            profile_id=1,
            system_id=24,  # Realtor.com
            access_token=None,
        )
        return user_external_id

    def main_function(self, locations: list[str] = None) -> None:
        # read locations from JSON configuration file
        if not locations:
            locations = self.read_locations_list_str_from_json()

        importer_ids = []
        all_inserted_ids = []

        for location in locations:
            # Get the links of all the listings
            listing_links = self.get_listing_links_from_location(location)
            curr_location_listings = self.wrapper_extract_data(listing_links)
            importer_id, inserted_ids = self.insert_to_table(curr_location_listings, location)
            importer_ids.append(importer_id)
            if isinstance(inserted_ids, int):
                inserted_ids = [inserted_ids]
            all_inserted_ids.extend(inserted_ids)

        return importer_ids, all_inserted_ids

    def __del__(self):
        self.driver.quit()
