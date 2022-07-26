import requests
import traceback
import threading
import time
import random


_DEFAULT_URL = 'https://www1.ufrgs.br/sistemas/sde/gerencia-documentos/index.php/publico/ExibirPDF?documento='
_THREADS = 10

def download_incrementing(from_id, to_id):
    current_id = from_id
    while current_id < to_id:
        if current_id % 100 == 0:
            print(current_id)

        url = _DEFAULT_URL + str(current_id)

        if random.random() < 0.1:
            time.sleep(60)

        try:
            # print(url)
            actual_response = requests.get(url)
            if is_target(actual_response):
                # print('Selected')
                save(actual_response, current_id)

        except Exception as e:
            print('Failed to request HEAD for ' + url)
            print(e)
            traceback.print_exc()
        # print('\n')
        current_id = current_id + _THREADS


def is_target(response):
    is_target = False
    for resp in response.history:
        # print(resp.status_code, resp.url)
        if resp.status_code == 302:
            is_target = True
    return is_target

def save(response, document_id):
    file_path = '../data/ufrgs/portarias/downloaded_pdfs/' + str(document_id) + '.pdf'
    # file_path = 'tmp/' + str(document_id) + '.pdf'
    with open(file_path, 'wb') as f:
        f.write(response.content)
        #print('Saving document with id' + str(document_id) + ' to disc.')


def download_all(from_id, to_id):
    threads = []
    for i in range(0, _THREADS):
        thread = threading.Thread(target=download_incrementing, args=(from_id + i, to_id))
        threads.append(thread)
        thread.start()
        print('Starting thread ' + str(i))
    
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    from_id_excluded = 18000
    to_id_included = 106000
    download_all(from_id_excluded, to_id_included)
    