import argparse
import os
import requests
import re
from bs4 import BeautifulSoup
import json
import zipfile
import configparser
from PIL import Image
import shutil
from datetime import datetime
from urllib.parse import unquote
import time

DEBUG_MODE = False


def download_image(url, output=None, cookies=None):
    if not isinstance(url, str):
        raise TypeError('Expected a string')

    headers = {
        'Referer': 'http://www.pixiv.net/'
    }

    response = requests.get(url, headers=headers, cookies=cookies)

    if response.status_code != 200:
        response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    debug_print(soup)

    # Extract the content of the meta tag with the ID 'meta-preload-data'
    meta_content = soup.find(
        'meta', {'id': 'meta-preload-data'}).get('content')

    # Load the content as a JSON object
    data = json.loads(meta_content)
    debug_print(data)

    # Extract number after "artworks/"
    match = re.search(r'artworks/(\d+)', url)
    debug_print(match)
    if not match:
        raise ValueError('No artwork ID found in URL')
    artwork_id = match.group(1)

    if 'illust' in data:
        for illust_id, illust_data in data['illust'].items():
            if 'userIllusts' in illust_data:
                debug_print("userIllusts in data for illust ID",
                            illust_id, ":", illust_data['userIllusts'])
                if artwork_id in illust_data['userIllusts']:
                    debug_print(
                        f"Found artwork in 'userIllusts' with ID {artwork_id}:")
                    artwork = illust_data['userIllusts'][artwork_id]
                    debug_print(f"Artwork: {artwork}")

                    if artwork.get('pageCount') > 1:
                        directory_path = os.path.join(
                            output if output else "", artwork_id)
                        if not os.path.exists(directory_path):
                            os.makedirs(directory_path)
                    else:
                        directory_path = output if output else ""
                        if not os.path.exists(directory_path):
                            os.makedirs(directory_path)

                    debug_print(f"Directory Path: {directory_path}")
                    debug_print(
                        f"Type of artwork: {artwork.get('illustType')}")

                    if artwork.get('illustType') == 0:
                        debug_print("0")
                        image = 0
                        while image < artwork.get('pageCount'):
                            artwork_url = artwork.get('url')
                            url = re.sub(
                                r'/c/250x250_80_a2/custom-thumb', '/img-master', artwork_url)
                            url = re.sub(
                                r'/c/250x250_80_a2/img-master', '/img-master', url)
                            url = re.sub(r'_square1200.jpg$',
                                         '_master1200.jpg', url)
                            url = re.sub(r'_custom1200.jpg$',
                                         '_master1200.jpg', url)
                            url = re.sub(r'p[0-9]+', f'p{image}', url)
                            debug_print(f"image url: {url}")
                            headers = {
                                'Referer': 'http://www.pixiv.net/'
                            }
                            response = requests.get(
                                url, headers=headers, cookies=cookies, stream=True)
                            debug_print(
                                f"Specific file download response: {response}")

                            if response.status_code == 200:
                                file_extension = os.path.splitext(url)[-1]
                                filename_image = image + 1
                                output = f"{artwork.get('id')} - {filename_image}{file_extension}"
                                debug_print(f"File name: {output}")
                                full_output_path = os.path.join(
                                    directory_path, output)
                                with open(os.path.join(full_output_path), 'wb') as out_file:
                                    out_file.write(response.content)
                                image = image + 1

                            else:
                                error_message = f"Unable to download image, server responded with status code: {response.status_code}"
                                debug_print(error_message)
                                raise Exception(error_message)

                    elif artwork.get('illustType') == 1:
                        debug_print("1")
                        image = 0
                        while image < artwork.get('pageCount'):
                            artwork_url = artwork.get('url')
                            url = re.sub(
                                r'/c/250x250_80_a2/custom-thumb', '/img-master', artwork_url)
                            url = re.sub(
                                r'/c/250x250_80_a2/img-master', '/img-master', url)
                            url = re.sub(r'_square1200.jpg$',
                                         '_master1200.jpg', url)
                            url = re.sub(r'_custom1200.jpg$',
                                         '_master1200.jpg', url)
                            url = re.sub(r'p[0-9]+', f'p{image}', url)
                            debug_print(f"image url: {url}")
                            headers = {
                                'Referer': 'http://www.pixiv.net/'
                            }
                            response = requests.get(
                                url, headers=headers, cookies=cookies, stream=True)
                            debug_print(
                                f"Specific file download response: {response}")

                            if response.status_code == 200:
                                file_extension = os.path.splitext(url)[-1]
                                filename_image = image + 1
                                output = f"{artwork.get('id')} - {filename_image}{file_extension}"
                                debug_print(f"File name: {output}")
                                full_output_path = os.path.join(
                                    directory_path, output)
                                with open(os.path.join(full_output_path), 'wb') as out_file:
                                    out_file.write(response.content)
                                image = image + 1

                            else:
                                error_message = f"Unable to download image, server responded with status code: {response.status_code}"
                                debug_print(error_message)
                                raise Exception(error_message)

                    elif artwork.get('illustType') == 2:
                        debug_print("2")
                        artwork_url = artwork.get('url')
                        url = re.sub(r'/c/250x250_80_a2/custom-thumb',
                                     '/img-zip-ugoira', artwork_url)
                        url = re.sub(r'/c/250x250_80_a2/img-master',
                                     '/img-zip-ugoira', url)
                        url = re.sub(r'_square1200.jpg$',
                                     '_ugoira600x600.zip', url)
                        url = re.sub(r'_custom1200.jpg$',
                                     '_ugoira600x600.zip', url)
                        debug_print(f"image url: {url}")
                        headers = {
                            'Referer': 'http://www.pixiv.net/'
                        }
                        response = requests.get(
                            url, headers=headers, cookies=cookies, stream=True)
                        debug_print(
                            f"Specific file download response: {response}")

                        if response.status_code == 200:
                            file_extension = os.path.splitext(url)[-1]
                            output = f"{artwork.get('id')}.zip"
                            debug_print(f"File name: {output}")

                            full_output_path = os.path.join(
                                directory_path, output)
                            with open(full_output_path, 'wb') as out_file:
                                out_file.write(response.content)

                            # Create a sub-directory for extracted files
                            extracted_folder = os.path.join(
                                directory_path, f"{artwork.get('id')}_extracted")
                            os.makedirs(extracted_folder, exist_ok=True)

                            # Unzipping the file into the sub-directory
                            debug_print(
                                f"Unzipping {full_output_path} into {extracted_folder}")
                            with zipfile.ZipFile(full_output_path, 'r') as zip_ref:
                                zip_ref.extractall(extracted_folder)

                            # Create GIF
                            debug_print("Creating GIF")
                            image_files = sorted([f for f in os.listdir(
                                extracted_folder) if f.endswith(('.jpg', '.png', '.jpeg'))])

                            images = []
                            for image_file in image_files:
                                image_path = os.path.join(
                                    extracted_folder, image_file)
                                images.append(Image.open(image_path))

                            gif_output_path = os.path.join(
                                directory_path, f"{artwork.get('id')}.gif")
                            images[0].save(
                                gif_output_path, save_all=True, append_images=images[1:], loop=0, duration=100)
                            debug_print(f"GIF created at {gif_output_path}")

                            # Delete the zip file and the extracted files
                            debug_print(
                                f"Deleting ZIP file: {full_output_path}")
                            os.remove(full_output_path)
                            debug_print(
                                f"Deleting extracted folder: {extracted_folder}")
                            shutil.rmtree(extracted_folder)

                        else:
                            error_message = f"Unable to download image, server responded with status code: {response.status_code}"
                            debug_print(error_message)
                            raise Exception(error_message)

    else:
        debug_print("Illust not found in data")


def download_tags(url, tag, sort_order, page_start, page_end, s_mode, type, ai_type, resolution, custom_resolution, ratio, period, bookmarks, file_location, cookies_psshid, debug, link):

    # https://www.pixiv.net/en/tags/%E9%A2%A8%E6%99%AF%E7%94%BB/illustrations?order=popular_d&s_mode=s_tag
    # default if not logged in:
    # https://www.pixiv.net/ajax/search/illustrations/%E9%A2%A8%E6%99%AF%E7%94%BB?word=風景画&order=date_d&mode=all&p=1&s_mode=s_tag_full&type=illust_and_ugoira
    # https://www.pixiv.net/ajax/search/illustrations/%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB?word=オリジナル&order=date_d&mode=all&p=3&s_mode=s_tag_full&type=illust_and_ugoira

    if cookies_psshid is None:
        if sort_order != 'newest' or \
           s_mode != 'perfect_match' or \
           type != 'illust_and_ugoira' or \
           ai_type != 'display_ai' or \
           resolution != 'all' or \
           ratio != 'all' or \
           period is not None or \
           bookmarks != 'all':
            print(
                "Either use the default settings for all arguments or provide a value for cookies_psshid.")
            exit(1)

    if link == "True":

        tag_match = re.search(r'/tags/([^/]+)/', url)
        if tag_match:
            encoded_tag = tag_match.group(1)
            decoded_tag = unquote(encoded_tag)
            debug_print(f"Tag: {decoded_tag}")
            tag = decoded_tag
        else:
            print("Tag not found in URL.")

        sort_order_match = re.search(r'order=([^&]+)', url)
        if sort_order_match:
            sort_order = sort_order_match.group(1)
            debug_print(f"Sort Order: {sort_order}")
        else:
            sort_order = 'date_d'
            debug_print(f"Sort Order: {sort_order}")

        if page_start is None:
            page_match = re.search(r'p=(\d+)', url)
            if page_match:
                page = page_match.group(1)
                debug_print(f"Page: {page}")
                page_start = int(page)
            else:
                page_start = 1
                debug_print(f"Page: {page_start}")

        if page_end is None:
            page_end = page_start
            debug_print(f"Page End: {page_end}")

        s_mode_match = re.search(r's_mode=([^&]+)', url)
        if s_mode_match:
            s_mode_value = s_mode_match.group(1)
            debug_print(f"s_mode value found: {s_mode_value}")
            s_mode = s_mode_value
        else:
            s_mode_value = 'perfect_match'
            debug_print(f"s_mode value found: {s_mode_value}")

        artworks_match = re.search(r'/artworks', url)
        if artworks_match:
            type = 'all'  # Set type to 'all' if '/artworks' is found
            debug_print(f"Type: {type}")
        else:
            # Look for '?type={type}' or '&type={type}' in the URL
            type_match = re.search(r'[?&]type=([^&]+)', url)
            if type_match:
                # Extract the value for 'type' if found
                type = type_match.group(1)
                debug_print(f"Type: {type}")
            else:
                type = 'illust_and_ugoira'  # Default value if neither 'artworks' nor 'type' is found
                debug_print(f"Type: {type}")

        ai_type_match = re.search(r'ai_type=([^&]+)', url)
        if ai_type_match:
            ai_type = ai_type_match.group(1)
            if ai_type == '1':
                ai_type = 'hide_ai'
            debug_print(f"AI Type: {ai_type}")
        else:
            ai_type = 'display_ai'
            debug_print(f"AI Type: {ai_type}")

        if custom_resolution is None:
            resolution_match = re.search(
                r'&wlt=(\d+)&wgt=(\d+)&hlt=(\d+)&hgt=(\d+)', url)
            if resolution_match:
                wlt, wgt, hlt, hgt = resolution_match.groups()
                resolution = f"{wlt}-{wgt}x{hlt}-{hgt}"
                debug_print(f"Resolution: {resolution}")
            else:
                resolution_match = re.search(r'&wlt=(\d+)&hlt=(\d+)', url)
                if resolution_match:
                    wlt, hlt = resolution_match.groups()
                    resolution = f"{wlt}x{hlt}"
                    debug_print(f"Resolution: {resolution}")
                else:
                    resolution_match = re.search(r'&wgt=(\d+)&hgt=(\d+)', url)
                    if resolution_match:
                        wgt, hgt = resolution_match.groups()
                        resolution = f"{wgt}x{hgt}"
                        debug_print(f"Resolution: {resolution}")
                    else:
                        resolution = 'all'
                        debug_print(f"Resolution: {resolution}")

        ratio_match = re.search(r'ratio=([-0-9.]+)', url)
        if ratio_match:
            ratio_value = float(ratio_match.group(1))
            if ratio_value == 0.5:
                ratio = "horizontal"
            elif ratio_value == -0.5:
                ratio = "vertical"
            elif ratio_value == 0:
                ratio = "square"
            else:
                ratio = "unknown"
            debug_print(f"Ratio: {ratio}")
        else:
            ratio = 'all'
            debug_print(f"Ratio: {ratio}")

        period_match = re.search(
            r'scd=(\d{4}-\d{2}-\d{2})&ecd=(\d{4}-\d{2}-\d{2})', url)
        if period_match:
            start_date = period_match.group(1)
            end_date = period_match.group(2)
            period = f"{start_date} to {end_date}"
            debug_print(f"Period: {period}")
        else:
            period = 'all'
            debug_print(f"Period: {period}")

        bookmark_match = re.search(r'blt=(\d+)', url)
        bookmark_gt_match = re.search(r'bgt=(\d+)', url)
        if bookmark_match and bookmark_gt_match:
            blt_value = bookmark_match.group(1)
            bgt_value = bookmark_gt_match.group(1)
            bookmarks = f"From {blt_value} to {bgt_value}"
            debug_print(f"Bookmarks: {bookmarks}")
        elif bookmark_match:
            blt_value = bookmark_match.group(1)
            bookmarks = f"{blt_value}+"
            debug_print(f"Bookmarks: {bookmarks}")
        else:
            bookmarks = 'all'
            debug_print(f"Bookmarks: {bookmarks}")

        if cookies_psshid is None:
            if sort_order != 'date_d' or \
                    s_mode != 's_tag_full' or \
                    type != 'illust_and_ugoira' or \
                    ai_type != 'display_ai' or \
                    resolution != 'all' or \
                    ratio != 'all' or \
                    period is not None or \
                    bookmarks != 'all':
                print(
                    "Either use the default settings for all arguments or provide a value for cookies_psshid.")
                exit(1)

    if tag is None:
        tag_match = re.search(r'/tags/([^/]+)/', url)
        if tag_match:
            encoded_tag = tag_match.group(1)
            decoded_tag = unquote(encoded_tag)
            debug_print(f"Tag: {decoded_tag}")
            tag = decoded_tag
        else:
            print("Tag required.")

    if sort_order == 'newest':
        sort_order = 'date_d'
        debug_print(f"Sort Order: {sort_order}")
    elif sort_order == 'oldest':
        sort_order = 'date'
        debug_print(f"Sort Order: {sort_order}")
    elif sort_order == 'popular_all':
        sort_order = 'popular_d'
        debug_print(f"Sort Order: {sort_order}")
    elif sort_order == 'popular_male':
        sort_order = 'popular_male_d'
        debug_print(f"Sort Order: {sort_order}")
    elif sort_order == 'popular_female':
        sort_order = 'popular_female_d'
        debug_print(f"Sort Order: {sort_order}")

    if s_mode == 'perfect_match':
        s_mode = 's_tag_full'
        debug_print(f"s_mode: {s_mode}")
    elif s_mode == 'partial_match':
        s_mode = 's_tag'
        debug_print(f"s_mode: {s_mode}")
    elif s_mode == 'title_caption':
        s_mode = 's_tc'
        debug_print(f"s_mode: {s_mode}")

    if ai_type == 'display_ai':
        ai_type = '0'
        debug_print(f"AI Type: {ai_type}")
    elif ai_type == 'hide_ai':
        ai_type = '1'
        debug_print(f"AI Type: {ai_type}")

    if resolution == 'all' and custom_resolution is None:
        resolution = None
        debug_print(f"Resolution: {resolution}")
    elif resolution == '3000x3000+' or resolution == '3000x3000':
        resolution = "&wlt=3000&hlt=3000"
        debug_print(f"Resolution: {resolution}")
    elif resolution == '1000x2999px' or resolution == "1000-2999x1000-2999":
        resolution = "&wlt=1000&wgt=2999&hlt=1000&hgt=2999"
        debug_print(f"Resolution: {resolution}")
    elif resolution == '<999x999' or resolution == "999x999":
        resolution = "&wgt=999&hgt=999"
        debug_print(f"Resolution: {resolution}")

    if custom_resolution is not None:
        res_match = re.match(r'(\d+)x?(\d*)-(\d+)x?(\d*)', custom_resolution)
        if res_match:
            wlt, hlt, wgt, hgt = res_match.groups()
            if wgt and hgt:
                resolution = f"&wlt={wlt}&wgt={wgt}&hlt={hlt}&hgt={hgt}"
            elif wlt and hlt:
                resolution = f"&wlt={wlt}&hlt={hlt}"
            debug_print(f"Custom Resolution: {resolution}")

    if ratio == 'all':
        ratio = None
        debug_print(f"Ratio: {ratio}")
    elif ratio == 'Horizontal':
        ratio = '&ratio=0.5'
        debug_print(f"Ratio: {ratio}")
    elif ratio == 'Vertical':
        ratio = '&ratio=-0.5'
        debug_print(f"Ratio: {ratio}")
    elif ratio == 'Square':
        ratio = '&ratio=0'
        debug_print(f"Ratio: {ratio}")

    if period == 'all':
        period = None
        debug_print(f"Period: {period}")
    elif period is not None:
        period_match = re.match(
            r'(\d{4}-\d{2}-\d{2})x(\d{4}-\d{2}-\d{2})', period)
        if period_match:
            start_date, end_date = period_match.groups()
            scd_ecd_str = f"&scd={start_date}&ecd={end_date}"
            period = scd_ecd_str
            debug_print(f"Start and End Dates: {scd_ecd_str}")
        else:
            debug_print(
                f"Invalid period format. Please provide in 'YYYY-MM-DDxYYYY-MM-DD' format.")

    if bookmarks == 'all':
        bookmarks = None
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '10000+':
        bookmarks = '&blt=10000'
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '5000-9999':
        bookmarks = '&blt=5000&bgt=9999'
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '1000-4999':
        bookmarks = '&blt=1000&bgt=4999'
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '500-999':
        bookmarks = '&blt=500&bgt=999'
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '300-499':
        bookmarks = '&blt=300&bgt=499'
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '100-299':
        bookmarks = '&blt=100&bgt=299'
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '50-99':
        bookmarks = '&blt=50&bgt=99'
        debug_print(f"Bookmarks: {bookmarks}")
    elif bookmarks == '30-49':
        bookmarks = '&blt=30&bgt=49'
        debug_print(f"Bookmarks: {bookmarks}")

    if type == 'illust_and_ugoira':
        type = f"https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}"
        debug_print(f"Type: {type}")
    elif type == 'illust':
        type = f"https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&type=illust"
        debug_print(f"Type: {type}")
    elif type == 'manga':
        type = f"https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&type=manga"
        debug_print(f"Type: {type}")
    elif type == 'ugoira':
        type = f"https://www.pixiv.net/ajax/search/illustrations/{tag}?word={tag}&type=ugoira"
        debug_print(f"Type: {type}")
    elif type == 'all':
        type = f"https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&type=all"
        debug_print(f"Type: {type}")

    request_url = type

    if sort_order:
        request_url = request_url + f"&order={sort_order}"
    if s_mode:
        request_url = request_url + f"&s_mode={s_mode}"
    if ai_type:
        request_url = request_url + f"&ai_type={ai_type}"
    if resolution:
        request_url = request_url + f"{resolution}"
    if ratio:
        request_url = request_url + f"{ratio}"
    if period:
        request_url = request_url + f"{period}"
    if bookmarks:
        request_url = request_url + f"{bookmarks}"

    debug_print(f"request_url: {request_url}")

    download_page(request_url, cookies_psshid,
                  file_location, page_start, page_end)

    debug_print("URL:", url)
    debug_print("Tag:", tag)
    debug_print("Sort Order:", sort_order)
    debug_print("Page Start:", page_start)
    debug_print("Page End:", page_end)
    debug_print("Search Mode:", s_mode)
    debug_print("Type:", type)
    debug_print("AI Type:", ai_type)
    debug_print("Resolution:", resolution)
    debug_print("Ratio:", ratio)
    debug_print("Period:", period)
    debug_print("Bookmarks:", bookmarks)
    debug_print("File Location:", file_location)
    debug_print("Cookies psshid:", cookies_psshid)
    debug_print("Debug:", debug)
    debug_print("Link:", link)


def download_page(url, cookies, file_location, page_start, page_end):

    prev_first_id = None
    last_error_page = None
    last_error_message = None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.pixiv.net',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
    }
    cookies = {'PHPSESSID': f'{cookies}'}

    for page in range(int(page_start), int(page_end) + 1):
        try:
            page_url = f"{url}&mode=all&p={page}"
            debug_print(f"Page URL: {page_url}")
            response = requests.get(page_url, cookies=cookies, headers=headers)
            data = response.json()
            debug_print(f"data: {data}")

            # Determine which key is present: 'illustManga', 'illust', or something else
            body_data = data.get('body', {})
            if 'illustManga' in body_data:
                debug_print("Data contains 'illustManga'")
                items = body_data['illustManga']['data']
                # continue processing with items from 'illustManga'
            elif 'illust' in body_data:
                debug_print("Data contains 'illust'")
                items = body_data['illust']['data']
                # continue processing with items from 'illust'
            else:
                debug_print("Neither 'illustManga' nor 'illust' found in data")

            first_id = items[0]['id']

            if prev_first_id is not None and prev_first_id == first_id:
                print(
                    'First ID from the previous request is the same as the current request.', page)
                break

            prev_first_id = first_id

            for item in items:
                print(
                    f"Downloading item: https://www.pixiv.net/en/artworks/{item['id']}, Title: {item['title']}, Page: {page}")

                debug_print(
                    "--------------------------------------------------")
                debug_print("Page: ", page)
                debug_print(
                    f"Page URL: https://www.pixiv.net/en/artworks/{item['id']}")
                debug_print(f"URL: {item['url']}")
                debug_print(f"ID: {item['id']}")
                debug_print(f"Page Count: {item['pageCount']}")
                debug_print(f"Title: {item['title']}")
                debug_print(f"Type: {item['illustType']}")

                if item['illustType'] == 2:
                    ugoira_url = f"https://www.pixiv.net/en/artworks/{item['id']}"
                    download_image(
                        ugoira_url, output=file_location, cookies=None)
                elif item['illustType'] == 1 or item['illustType'] == 0:
                    image_or_manga_url = f"https://www.pixiv.net/en/artworks/{item['id']}"
                    download_image(image_or_manga_url,
                                   output=file_location, cookies=None)

        except Exception as e:
            print(f"An error occurred on page {page}: {e}")

            # If the error happened on the same page as the last error
            if last_error_page == page and str(last_error_message) == str(e):
                print(
                    "The same error occurred twice in a row on the same page. Stopping the script.")
                break

            # Otherwise, update the last error page and message
            last_error_page = page
            last_error_message = e

            print("An error occurred. Waiting for 10 minutes before trying again.")
            time.sleep(10)  # Wait for 10 minutes
    print("Done")


def debug_print(*args, **kwargs):
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")  # Get the current date and time
    if DEBUG_MODE:
        with open("debug.log", "a", encoding="utf-8") as f:
            # Print the timestamp before the actual debug line
            print(f"[{timestamp}] ", end="", file=f)
            print(*args, file=f, **kwargs)
            print("--------------------------------------", file=f)
        # Print the timestamp before the actual debug line
        print(f"[{timestamp}] ", end="")
        print(*args, **kwargs)
        print("-------------------------------------------")


def main(args):
    global DEBUG_MODE
    DEBUG_MODE = args.debug

    if args.tag is not None or args.url.startswith("https://www.pixiv.net/en/tags/"):
        print('Downloading tags...')
        download_tags(args.url, args.tag, args.sort_order, args.page_start, args.page_end, args.s_mode, args.type, args.ai_type, args.resolution,
                      args.custom_resolution, args.ratio, args.period, args.bookmarks, args.file_location, args.cookies_psshid, args.debug, args.link)
    elif args.url.startswith("https://www.pixiv.net/en/artworks"):
        print("Downloading image...")
        download_image(args.url, output=args.file_location)


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config['DEFAULT']


def cli_main(args=None):
    parser = argparse.ArgumentParser(description='Process Pixiv URL.')
    parser.add_argument('url', help='The Pixiv URL to process.', nargs='?')

    parser.add_argument('--tag', default=None,
                        help='OPTIONAL Tag associated with the URL.')
    parser.add_argument('--sort_order', default='newest', choices=[
                        'newest', 'oldest', 'popular_all', 'popular_male', 'popular_female'], help='Sort order for results.')
    parser.add_argument('--page_start', type=int,
                        help="Page number to start", default=None)
    parser.add_argument('--page_end', type=int,
                        help="Page number to end", default=None)
    parser.add_argument('--s_mode', default='perfect_match', choices=[
                        'perfect_match', 'partial_match', 'title_caption'], help='Mode for the tag search.')

    parser.add_argument('--type', default='illust_and_ugoira', choices=[
                        'all', 'illust_and_ugoira', 'illust', 'manga', 'ugoira'], help='Type of content.')

    parser.add_argument('--ai_type', default='display_ai',
                        choices=['display_ai', 'hide_ai'], help='AI type.')
    parser.add_argument('--resolution', default='all', choices=[
                        'all', '3000x3000+', '1000x2999px', '<999x999'], help='Resolution filter.')
    parser.add_argument('--custom_resolution', default=None, type=str,
                        help='Custom resolution format "widthxheight-widthxheight"')
    parser.add_argument('--ratio', default='all',
                        choices=['all', 'Horizontal', 'Vertical', 'Square'], help='Ratio filter.')
    parser.add_argument('--period', default=None,
                        help='Period in the format "YYYY-MM-DDxYYYY-MM-DD".')
    parser.add_argument('--bookmarks', default='all', choices=['all', '10000+', '5000-9999',
                        '1000-4999', '500-999', '300-499', '100-299', '50-99', '30-49'], help='Bookmark range.')

    parser.add_argument('--config', default=None, const='./config.ini', nargs='?',
                        help='Path to the config file. If the flag is provided with no path, defaults to ./config.ini.')
    parser.add_argument('--file_location', default='./',
                        help='Path where files should be stored.')
    parser.add_argument('--cookies_psshid', default=None,
                        help='Cookies psshid value.')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode.')
    parser.add_argument('--link', default="False",
                        help='Get configuration from link.')

    args = parser.parse_args()

    if args.config:
        if os.path.exists(args.config):
            config = read_config(args.config)
            for key, value in config.items():
                if key == 'debug':
                    value = value.lower() == 'true'
                setattr(args, key, value)
        else:
            print(f"Config file {args.config} does not exist.")
            exit(1)

    elif args.url is None:  # No URL and no --config
        print("Either URL or --config must be specified.")
        exit(1)

    main(args)


##
# WORK ON FINDING OUT THE INFO FROM THE URL
# https://www.pixiv.net/en/tags/%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB/illustrations?order=popular_male_d&scd=2023-08-22&ecd=2023-08-29&blt=1000&bgt=4999&s_mode=s_tag&wlt=1000&wgt=2999&hlt=1000&hgt=2999&ratio=0&ai_type=1
# priorities: mentioned in --arguments, url
# write code to decode what arguments may be in url
if __name__ == "__main__":
    cli_main()
