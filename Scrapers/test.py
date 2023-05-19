from datetime import datetime, timedelta

list = ["hola"]
print(len(list))

# First column with hyperlink
    hyperlink = cols[0].find_element(By.TAG_NAME, "a").get_attribute('href')

    # Fourth column with text
    # Ensure there are at least four columns
    if len(cols) >= 4:
        text = cols[3].text

        # append data
        data.append([hyperlink, text])
    else:
        print("Row didn't have 4 columns")




