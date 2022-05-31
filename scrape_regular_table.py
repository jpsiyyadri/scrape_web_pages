from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd



# tr -> row
# td -> column inside body
# th -> column inside header (highlight and bolds text -> ref: same as excel headers)


'''
Structure of the input page
    table
        thead
            tr
                th Industry region
                th 2017
                th 2018
        tbody
            tr
                td Total
                td 43.3
                td 44.5
---------------------------------------
Structure of the output response
    Total, 2017, 43.3
    Total, 2018, 44.5
'''


def extract_data(url, ignore_rows=0, ignore_columns_start=0, ignore_columns_end=0):
    page = req.get(url) # hit the url
    html = page._content # read the page coontents
    soup = bs(html, 'html.parser') # pars the contents of the page

    table = soup.find("table") # get the table element
    thead = table.find("thead") # get the thead of the table
    tbody = table.find("tbody") # get the tbody of the table


    thead_meta = {} # store all the column information
    for tr in thead.findAll("tr"):
        idx = 1
        all_ths = tr.findAll("th")[1:]
        if(ignore_columns_start > 0):
            all_ths = all_ths[ignore_columns_start:]
        if(ignore_columns_end > 0):
            all_ths = all_ths[0:-ignore_columns_end]
        
        for th in all_ths:
            thead_meta[idx] = th.text
            idx += 1

    store_the_output = []

    all_trs = tbody.findAll("tr") # get all the trs from tbody
    if(ignore_rows > 0):
        all_trs = all_trs[0:-ignore_rows] # if we have 100 rows and you don't want last 6 rows then 0:-6 will give you first 94 rows

    for tr in all_trs: # iterate through all the trs in the tbody
        industry_and_region = tr.findAll("th")[0].text # get the name of the Industry or region from the first column(th)
        print(industry_and_region)

        all_tds = tr.findAll("td") # get all the tds in each tr

        if(ignore_columns_start > 0):
            all_tds = all_tds[ignore_columns_start+1:]

        if(ignore_columns_end > 0):
            all_tds = all_tds[0:-ignore_columns_end]

        if(len(all_tds)): # if tr has tds then go ahead
            idx = 1
            for td in all_tds: # iterate through each td
                text_of_td = td.text # get the text in each td
                if(text_of_td): # if the text inside td is not empty then go ahead
                    store_obj = {
                        "industy": industry_and_region,
                        "val": td.text,
                        "year": thead_meta[idx]
                    }
                    store_the_output.append(store_obj)
                else: # if the text inside td is empty then do nothing
                    print("empty td found in tr > ", tr)
                idx += 1
        else: # if tr has no tds then do nothing
            print("we don't have any tds under this")
            print(tr)
            print("%"*100)
    return store_the_output


def export_the_output(output):
    df = pd.DataFrame(output)
    df.to_excel("rajesh_op.xlsx")
    print("Successfully exported!!!")

yearwise_data_url = "https://www.bls.gov/news.release/jolts.t16.htm#"
output = extract_data(yearwise_data_url, 6)
export_the_output(output)


# monthwise_data_url = "https://www.bls.gov/news.release/jolts.t09.htm"
# monthwise_output = extract_data(monthwise_data_url, 6, 2)
# export_the_output(monthwise_output)
