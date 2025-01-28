from telethon import TelegramClient, events
import time 
import ast
import re

api_id = 1111111 # #Personal information from telegram api
api_hash = '#' #Personal information from telegram api

client = TelegramClient('anon', api_id, api_hash)#Passing all necessary values ​​to the session client
client.start()#Start of bot session

#Сreating the necessary variables for processing-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

list_with_forwards = dict({1: {'from': 'stubb', 'to': 'stubb'}, 2: {'from': 'stubb', 'to': 'stubb'}, 3: {'from': 'stubb', 'to': 'stubb'}, 4: {'from': 'stubb', 'to': 'stubb'}, 5: {'from': 'stubb', 'to': 'stubb'}, 6: {'from': 'stubb', 'to': 'stubb'}, 7: {'from': 'stubb', 'to': 'stubb'}, 8: {'from': 'stubb', 'to': 'stubb'}, 9: {'from': 'stubb', 'to': 'stubb'}, 10: {'from': 'stubb', 'to': 'stubb'}, 11: {'from': 'stubb', 'to': 'stubb'}, 12: {'from': 'stubb', 'to': 'stubb'}, 13: {'from': 'stubb', 'to': 'stubb'}, 14: {'from': 'stubb', 'to': 'stubb'}, 15: {'from': 'stubb', 'to': 'stubb'}, 16: {'from': 'stubb', 'to': 'stubb'}, 17: {'from': 'stubb', 'to': 'stubb'}, 18: {'from': 'stubb', 'to': 'stubb'}, 19: {'from': 'stubb', 'to': 'stubb'}, 20: {'from': 'stubb', 'to': 'stubb'}})#A variable that stores all data about the notification redirection settings
list_fro_save_coments = dict({1: {'coment': 'none'}, 2: {'coment': 'none'}, 3: {'coment': 'none'}, 4: {'coment': 'none'}, 5: {'coment': 'none'}, 6: {'coment': 'none'}, 7: {'coment': 'none'}, 8: {'coment': 'none'}, 9: {'coment': 'none'}, 10: {'coment': 'none'}, 11: {'coment': 'none'}, 12: {'coment': 'none'}, 13: {'coment': 'none'}, 14: {'coment': 'none'}, 15: {'coment': 'none'}, 16: {'coment': 'none'}, 17: {'coment': 'none'}, 18: {'coment': 'none'}, 19: {'coment': 'none'}, 20: {'coment': 'none'}})
from_chenal_name = str()#Variable in which the chat sender is temporarily stored
to_chenal_name = str()#Variable in which the recipient's chat is temporarily stored
delate_tokin_name = str()#Temporary storage of a name that requires deletion
counter = int()#An important counter for correctly filling out the main dictionary and also serves as a limiter
list_for_stop_treak = list()#List to store items to stop message forwarding for a specific chat channel
list_for_check_repetitions = list()#A variable to avoid sending the same address many times

#Opening a file to obtain data about the dictionary included in the file-------------------------------------------------------------------------------------------------------------------------------------------------------------

with open("File_to_save_information_on_reboot.txt", "r") as file1:
    data = file1.read()
    
with open("variable_storage_file.txt", "r") as file1:
    data_of_counter = file1.read()

with open("File_to_sleap_trecing_proces.txt", "r") as file1:
    data_of_sleep_elements = file1.read()

with open("save_coments.txt", "r") as file1:
    coments_data = file1.read()


try:# Converting a string to a dictionary
    
    result_dict = ast.literal_eval(data)
    list_with_forwards = result_dict
    result_dict = None
    
except Exception as err:
    print(f"Ошибка при обработке данных: {err}")

try :#Converting data and passing data to count variable
    counter = int(data_of_counter)
    data_of_counter = None

except Exception as err:
    print(f"Ошибка при обработке данных: {err}")

try:# Converting a string to a dictionary
    list_for_stop_treak = ast.literal_eval(data_of_sleep_elements)
    data_of_sleep_elements = None
    
except Exception as err:
    print(f"Ошибка при обработке данных: {err}")

try:# Converting a string to a dictionary
    
    coments_data = ast.literal_eval(coments_data)
    list_fro_save_coments = coments_data
    coments_data = None
    
except Exception as err:
    print(f"Ошибка при обработке данных: {err}")

#Function for processing crypto wallets of different types-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def extract_wallet_addresses(message):

    """Function for processing crypto wallets of different types"""

    # Define patterns for different wallet types
    patterns = {"Bitcoin": r"\b(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}\b","Ethereum": r"\b0x[a-fA-F0-9]{40}(?:[a-fA-F0-9]{24})?(?:::[a-zA-Z0-9]+::[a-zA-Z0-9]+)?\b","Solana": r"\b[a-zA-HJ-NP-Z0-9]{44}\b"}

    # Pattern to match URLs containing wallet addresses
    wallet_url_pattern = r"(https?://[^\s/]+/[^\s/]+/(0x[a-fA-F0-9]{40}|[1-3][a-zA-HJ-NP-Z0-9]{25,39}|[a-zA-HJ-NP-Z0-9]{44}))"

    # Dictionary to store found wallet addresses and links
    found_addresses = {wallet: [] for wallet in patterns}
    found_links = []

    wallet_links = re.findall(wallet_url_pattern, message)

    # Search for wallet links
    if wallet_links:
        for link, wallet in wallet_links:
            found_links.append({"link": link, "wallet": wallet})

    # Remove wallet URLs from content to avoid duplicate detection
    content_without_wallet_urls = re.sub(wallet_url_pattern, "", message)

    # Search for standalone wallet addresses in the remaining content
    for wallet, pattern in patterns.items():
        matches = re.findall(pattern, content_without_wallet_urls)
        found_addresses[wallet].extend(matches)

    return found_addresses, found_links

#Function for setting up forwarding in the bot-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.on(events.NewMessage('@you_public_chenal_name'))
async def main(event) -> None:

    """The function was created to configure forwarding from one channel to another. Using it, you can choose from where and where the message will be forwarded"""#Docs

    global list_with_forwards, from_chenal_name, to_chenal_name, delate_tokin_name, counter, list_fro_save_coments, list_for_stop_treak

#Creating detailed documentation for working with bot setup------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if event.text == "help" or event.text == "Help" or event.text == "/help" or event.text == "/Help" :
        await client.send_message('@you_public_chenal_name', 'Commands supported by the Scraper Bot\n\n"from" - add new from and to order\n\n"id" - add new from and to order via chat id\n\n"dell" - delete from and to order\n\n"show" - view list of created orders\n\n"stop" - stop tracking the specified order\n\n"dell stop" - track the specified order again\n\n"user" - add user to the order via id/pre-id\n\n"turn off" - stop the bot for 1 minute\n\nTo open an extended tooltip, use the command you want to specify and put a slash in front of the command /\n\nExample: /help')

    if event.text == "/from" or event.text == "/From":
        await client.send_message('@you_public_chenal_name', """From = source, to = destination 🚀\n\nWorks for public chats/channels only\n\nExample: from @chat to @bot""")

    if event.text == "/dell" or event.text == "/Dell":
        await client.send_message('@you_public_chenal_name', """To delete the order, write dell and specify its number\n\nExample: dell 1""")

    if event.text == "show" or event.text == "Show" or event.text == "/show" or event.text == "/Show":
        if counter > 0:
            for i in range(1, counter+1):
                if len(list_with_forwards[i])!=3:
                    if i in list_for_stop_treak:
                        await client.send_message('@you_public_chenal_name', f"""❌{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} with comment: {list_fro_save_coments[i]["coment"]}""")
                    
                    else :
                        await client.send_message('@you_public_chenal_name', f"""✅{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} with comment: {list_fro_save_coments[i]["coment"]}""")

                else :
                    if i in list_for_stop_treak:
                        await client.send_message('@you_public_chenal_name', f"""❌{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} only receive from\n\n➡️{list_with_forwards[i]['id']} with comment: {list_fro_save_coments[i]["coment"]}""")

                    else :
                        await client.send_message('@you_public_chenal_name', f"""✅{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} only receive from\n\n➡️{list_with_forwards[i]['id']} with comment: {list_fro_save_coments[i]["coment"]}""")
        else :
            await client.send_message('@you_public_chenal_name', """‼️You haven't added any redirects""")

    if event.text == "/user" or event.text == "/User":
                await client.send_message('@you_public_chenal_name', f"""Add user to the order via id/pre-id\n\nGet ID here -> @username_to_id_bot\n\nIf the admin is texting on behalf of the chat, you need to take the pre-id from the link to his message\n\nExample: user 1234567 to 1""")

    if event.text == "/id" or event.text == "/Id":
            await client.send_message('@you_public_chenal_name', f"""From = source id, to = destination username/id. \n\nGet IDs here -> @username_to_id_bot\n\nleaving a comment on the item is optional\n\nExample: from id to @bot/id""")

    if event.text == "/stop" or event.text == "/Stop":
        await client.send_message('@you_public_chenal_name', f"""To stop the order, write stop and specify its number\n\nExample: stop 1""")

    if event.text == "/dell stop" or event.text == "/Dell stop":
        await client.send_message('@you_public_chenal_name', f"""To track order again, write dell stop and specify its number\n\nExample: dell stop 1""")

    if event.text == "turn off" or event.text == "Turn off":
        await client.send_message('@you_public_chenal_name', f"""‼️A complete shutdown of the bot was applied for 1 minet‼️""")
        time.sleep(60)#The bot stops for 1 minet
        await client.send_message('@you_public_chenal_name', f"""‼️The bot is turned on after being disabled for 1 minet and is ready to work‼️""")
        
        exit()#Interrupting the compilation process to clear the cache

#Processing adding tracking-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if event.text[0] == "f" or event.text[0] == "F" and event.text[1] == "r" and event.text[2] == "o" and event.text[3] == "m" and len(list_with_forwards) == 20:#Receiving values ​​from the user and converting them into the desired form
        try :
            var_to_catch_name_of_chenal = ""#A variable that records the name of the receiver and sender channel
            switcher = False#Switch for not writing extra values ​​into the name
            svich_diget = 0

            coment_tempruar = ""
            coment_counter = 0
            coment_take = []

            for i in event.text:
                if svich_diget == 2 and i == " ":

                    try :#Receiving comments if it is present in the text that we received from the user
                        for i in event.text:

                            coment_counter+=1

                            coment_tempruar+=i

                            if i == " " or len(event.text) == coment_counter:
                                coment_take.append(coment_tempruar)
                                coment_tempruar = ""

                        del(coment_take[0])
                        del(coment_take[0])
                        del(coment_take[0])
                        del(coment_take[0])

                        for i in coment_take:
                            coment_tempruar += i

                        if coment_tempruar == " " or coment_tempruar == "":
                            coment_tempruar = "none"


                    except Exception as err:
                        await client.send_message('@you_public_chenal_name', f"""❌No comment added❌""")
                        print(err)
                        break

                    break#End receiving comments if it is present in the text that we received from the user
                    
                if i == "@":#In order to understand that the name of the element we are looking for begins
                    switcher = True
                    var_to_catch_name_of_chenal = ""
                    svich_diget += 1
                    
                if i == " ":#To avoid writing unnecessary values ​​inside a named variable
                    switcher = False
                    from_chenal_name = var_to_catch_name_of_chenal
                    

                if switcher == True:
                    var_to_catch_name_of_chenal += i
            to_chenal_name = var_to_catch_name_of_chenal

# Yes add functionall-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            if len(from_chenal_name) > 4 and len(to_chenal_name) and len(list_with_forwards) == 20:
                counter+=1
                list_with_forwards[counter] = {}#Preliminary creation of an element in the dictionary
                list_with_forwards[counter].update({"from":from_chenal_name, "to":to_chenal_name})#Adding an item to a dictionary

                if len(coment_tempruar) != 0:
                    list_fro_save_coments[counter] = {}#Preliminary creation of an element in the dictionary
                    list_fro_save_coments[counter].update({"coment":coment_tempruar})#Adding an item to a dictionary
                
                else :
                    list_fro_save_coments[counter] = {}#Preliminary creation of an element in the dictionary
                    list_fro_save_coments[counter].update({"coment":"none"})#Adding an item to a dictionary
                
            else :
                print(2/0)#Interrupt the execution of a function to satisfy the condition correctly

            with open("File_to_save_information_on_reboot.txt", "w") as file1:#Writing a dictionary update to a text file
                file1.write(f"{list_with_forwards}")

            with open("variable_storage_file.txt", "w") as file1:#Saving a count variable to a text file
                file1.write(f"{counter}")

            with open("save_coments.txt", "w") as file1:#Writing a dictionary update to a text file
                file1.write(f"{list_fro_save_coments}")

            await client.send_message('@you_public_chenal_name', f"""✅Everything was added correctly!\n\n‼️It was added: from {from_chenal_name} to {to_chenal_name}""")
            
            if counter > 0:
                for i in range(1, counter+1):
                    if len(list_with_forwards[i])!=3:
                        if i in list_for_stop_treak:
                            await client.send_message('@you_public_chenal_name', f"""❌{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} with comment: {list_fro_save_coments[i]["coment"]}""")
                        
                        else :
                            await client.send_message('@you_public_chenal_name', f"""✅{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} with comment: {list_fro_save_coments[i]["coment"]}""")

                    else :
                        if i in list_for_stop_treak:
                            await client.send_message('@you_public_chenal_name', f"""❌{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} only receive from\n\n➡️{list_with_forwards[i]['id']} with comment: {list_fro_save_coments[i]["coment"]}""")

                        else :
                            await client.send_message('@you_public_chenal_name', f"""✅{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} only receive from\n\n➡️{list_with_forwards[i]['id']} with comment: {list_fro_save_coments[i]["coment"]}""")

            exit()#Interrupting the compilation process to clear the cache
        
        except Exception as err:
            await client.send_message('@you_public_chenal_name', """You have not specified the value to be added❌""")

#Processing deletion tracking-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   
    if len(event.text) < 7 and event.text[0] == "d" and event.text[1] == "e" and event.text[2] == "l" and event.text[3] == "l" or len(event.text) < 7 and event.text[0] == "D" and event.text[1] == "e" and event.text[2] == "l" and event.text[3] == "l":#Receiving values ​​from the user and converting them into the desired form
        try :
            switcher = False#Switch for not writing extra values ​​into the name

            for i in event.text:
                if i == " ":#In order to understand that the name of the element we are looking for begins
                    var_to_catch_name_of_chenal_to_dellate = ""#A variable that records the name of the receiver and sender channel
                    switcher = True

                if switcher == True:
                    var_to_catch_name_of_chenal_to_dellate += i
            delate_tokin_name = var_to_catch_name_of_chenal_to_dellate

# Yes dell functionall--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
            if counter == 0 or counter<int(delate_tokin_name):#New--------------
                print(2/0)#Interrupt the execution of a function to satisfy the condition correctly

            chenge_numbers_in_main_dict = dict()#temporary variable to store data
            local_counter = int()#temporary variable to store data

            list_for_stop_treak_tempurary = []

            del list_with_forwards[int(delate_tokin_name)]

            for i in list_with_forwards:#Construction for correct replacement of a sequence of values occurs when an element is removed from the dict
                local_counter+=1
                chenge_numbers_in_main_dict[local_counter] = {}#Preliminary creation of an element in the dictionary
                chenge_numbers_in_main_dict[local_counter].update(list_with_forwards[i])#Adding an item to a dictionary

            counter-=1

            list_with_forwards = chenge_numbers_in_main_dict

            list_with_forwards[20] = {}#Pre-allocating memory in the dictionary to record values

            list_with_forwards[20].update({"from":"stubb", "to":"stubb"})#Adding a new element in place of the deleted one so that there are always 5 values


            chenge_numbers_comenst = dict()#temporary variable to store data
            local_counter_coments = int()#temporary variable to store data


            del list_fro_save_coments[int(delate_tokin_name)]

            for i in list_fro_save_coments:#Construction for correct replacement of a sequence of values occurs when an element is removed from the dict
                local_counter_coments+=1
                chenge_numbers_comenst[local_counter_coments] = {}#Preliminary creation of an element in the dictionary
                chenge_numbers_comenst[local_counter_coments].update(list_fro_save_coments[i])#Adding an item to a dictionary

            list_fro_save_coments = chenge_numbers_comenst

            list_fro_save_coments[20] = {}#Pre-allocating memory in the dictionary to record values

            list_fro_save_coments[20].update({"coment":"none"})#Adding a new element in place of the deleted one so that there are always 5 values
            

            with open("File_to_save_information_on_reboot.txt", "w") as file1:#Writing a dictionary update to a text file
                file1.write(f"{list_with_forwards}")

            with open("variable_storage_file.txt", "w") as file1:#Saving a count variable to a text file
                file1.write(f"{counter}")
            
            with open("save_coments.txt", "w") as file1:#Writing a dictionary update to a text file
                file1.write(f"{list_fro_save_coments}")
            
            if int(delate_tokin_name) in list_for_stop_treak:
                list_for_stop_treak.remove(int(delate_tokin_name))#Rewriting elements to the main data array


            if len(list_for_stop_treak) != 0:
                for i in list_for_stop_treak:#Correction of tokens that are in the list to stop tracking
                    if int(i) > int(delate_tokin_name):
                        list_for_stop_treak_tempurary.append(int(i)-1)
                    
                    else :
                        list_for_stop_treak_tempurary.append(int(i))#End correction of tokens that are in the list to stop tracking
                        
                list_for_stop_treak = list_for_stop_treak_tempurary
                
            with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                file1.write(f"{list_for_stop_treak}")

            await client.send_message('@you_public_chenal_name', f"""✅Everything was deleted correctly!\n\n‼️It was deleted: {delate_tokin_name}""")

            if counter > 0:
                for i in range(1, counter+1):
                    if len(list_with_forwards[i])!=3:
                        if i in list_for_stop_treak:
                            await client.send_message('@you_public_chenal_name', f"""❌{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} with comment: {list_fro_save_coments[i]["coment"]}""")
                        
                        else :
                            await client.send_message('@you_public_chenal_name', f"""✅{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} with comment: {list_fro_save_coments[i]["coment"]}""")

                    else :
                        if i in list_for_stop_treak:
                            await client.send_message('@you_public_chenal_name', f"""❌{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} only receive from\n\n➡️{list_with_forwards[i]['id']} with comment: {list_fro_save_coments[i]["coment"]}""")

                        else :
                            await client.send_message('@you_public_chenal_name', f"""✅{i})From {list_with_forwards[i]['from']} to {list_with_forwards[i]['to']} only receive from\n\n➡️{list_with_forwards[i]['id']} with comment: {list_fro_save_coments[i]["coment"]}""")
            else :
                await client.send_message('@you_public_chenal_name', """‼️You haven't added any redirects‼️""")

            exit()#Interrupting the compilation process to clear the cache

        except Exception as err:
            await client.send_message('@you_public_chenal_name', """You did not specify the value to be removed❌""")

#Processing information about receiving messages only from a specific user-----------------------------------------------------------------------------------------------------------------------------------------------

    if event.text[0] == "u" or event.text[0] == "U" and event.text[1] == "s" and event.text[2] == "e" and event.text[3] == "r":#Adding a User ID
        try :
            count = 0#Variable to switch
            userName = ""#Variable for processing id
            switcher = False#Switch for not writing extra values ​​into the name

            for i in event.text:

                if switcher == True and count == 1:

                    if i != " " and i!="*":
                        userName+=i
                    
                if i == " ":
                    switcher = True
                    count+=1

                if count == 3:
                    if i!="*":
                        toId = i

            if int(toId) > counter:#New--------------
                print(2/0)#Interrupt the execution of a function to satisfy the condition correctly

            if len(list_with_forwards[int(toId)]) !=3 :
                list_with_forwards[int(toId)].update({"id":[]})

            list_with_forwards[int(toId)]["id"].append(str(userName))#Adding an item to a dictionary
            print(list_with_forwards)

            with open("File_to_save_information_on_reboot.txt", "w") as file1:#Writing a dictionary update to a text file
                file1.write(f"{list_with_forwards}")

            await client.send_message('@you_public_chenal_name', f"""✅Everything was added correctly {list_with_forwards[int(toId)]["id"]}""")
            
            exit()#Interrupting the compilation process to clear the cache

        except Exception as err:
            if event.text != "user id":
                await client.send_message('@you_public_chenal_name', """Something went wrong❌""")

#An expression that helps parse id and use id for parsing-----------------------------------------------------------------------------------------------------------------------------------------------------------------

    if event.text[0] == "i" and event.text[1] == "d" or event.text[0] == "I" and event.text[1] == "d":
        try :
            switcher = False#Switch for not writing extra values ​​into the name
            counter+=1
            cot = 0#Variable to switch
            nana = ""#Variable for processing id
            userId = ""#Variable for processing id

            coment_counter = 0
            coment_tempruar = ""
            coment_take = []

            for i in event.text:
                if switcher == True and cot == 1:

                    if i != " " and i!="*":
                        userId+=i
                    
                if i == " ":
                    switcher = True
                    cot+=1

                if cot == 3: 
                    if i != " " and i!="*":
                        nana += i

            try :
                for i in event.text:

                    coment_counter+=1

                    coment_tempruar+=i

                    if i == " " or len(event.text) == coment_counter:
                        coment_take.append(coment_tempruar)
                        coment_tempruar = ""

                del(coment_take[0])
                del(coment_take[0])
                del(coment_take[0])
                del(coment_take[0])

                for i in coment_take:
                    coment_tempruar += i
                if coment_tempruar == " " or coment_tempruar == "":
                    coment_tempruar = "none"


            except Exception as err:
                print(err)

            if userId=="" and nana=="":
                counter-=1
                print(2/0)#Interrupt the execution of a function to satisfy the condition correctly

            list_with_forwards[counter] = {}#Preliminary creation of an element in the dictionary
            list_with_forwards[counter].update({"from":str(userId), "to": str(nana)})#Adding an item to a dictionary

            list_fro_save_coments[counter] = {}#Preliminary creation of an element in the dictionary
            list_fro_save_coments[counter].update({"coment":coment_tempruar})#Adding an item to a dictionary

            with open("File_to_save_information_on_reboot.txt", "w") as file1:#Writing a dictionary update to a text file
                file1.write(f"{list_with_forwards}")

            with open("variable_storage_file.txt", "w") as file1:#Saving a count variable to a text file
                file1.write(f"{counter}")

            with open("save_coments.txt", "w") as file1:#Writing a dictionary update to a text file
                file1.write(f"{list_fro_save_coments}")

            await client.send_message('@you_public_chenal_name', f"""✅Everything was added correctly {list_with_forwards[counter]["from"]} to {list_with_forwards[counter]["to"]} with comment: {list_fro_save_coments[counter]["coment"]}""")

            exit()#Interrupting the compilation process to clear the cache
        
        except Exception as err:
            await client.send_message('@you_public_chenal_name', """Something went wrong, try again!❌""")

#The function that is responsible for stopping the track of elements---------------------------------------------------------------------------------------------------------------------------------------------------------
    try:

        if len(event.text) > 4 and len(event.text) < 8 and event.text[0] == "s" and event.text[1] == "t" and event.text[2] == "o" and event.text[3] == "p" and event.text[4] == " " or len(event.text) > 4 and len(event.text) < 8 and event.text[0] == "S" and event.text[1] == "t" and event.text[2] == "o" and event.text[3] == "p" and event.text[4] == " ":
        
            temporary_variable_to_receive = str()#Variable for collecting data about the element that requires stopping

            for i in event.text:
                if i.isdigit():
                    temporary_variable_to_receive += i #Saving a sleep variable to into a temporary variable

            if counter < int(temporary_variable_to_receive) and counter!=0:
                print(print(2/0))#Interrupt the execution of a function to satisfy the condition correctly

            if not int(temporary_variable_to_receive) in list_for_stop_treak and counter >= int(temporary_variable_to_receive):
                list_for_stop_treak.append(int(temporary_variable_to_receive))#Rewriting elements to the main data array

                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                    file1.write(f"{list_for_stop_treak}")

                await client.send_message('@you_public_chenal_name', f"""✅Everything was added correctly apply stop for element number {int(temporary_variable_to_receive)}""")

            else :
                print(2/0)#Interrupt the execution of a function to satisfy the condition correctly

            exit()#Interrupting the compilation process to clear the cache

    except Exception as err:
        if str(err) == "string index out of range":
            pass

        else :
            await client.send_message('@you_public_chenal_name', """Something went wrong, try again!❌""")

#Removing elements from the array of elements that are responsible for temporarily stopping the transfer--------------------------------------------------------------------------------------------------------------------
    try:

        if len(event.text) > 9 and event.text[0] == "d" and event.text[1] == "e" and event.text[2] == "l" and event.text[3] == "l"  and event.text[5] == "s" and event.text[6] == "t" and event.text[7] == "o" and event.text[8] == "p" and event.text[4] == " ":
            
            temporary_variable_to_receive = str()#Variable for collecting data about the element that requires stopping
            
            for i in event.text:
                if i.isdigit():
                    temporary_variable_to_receive += i #Saving a sleep variable to into a temporary variable
            
            list_for_stop_treak.remove(int(temporary_variable_to_receive))#Rewriting elements to the main data array

            with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                file1.write(f"{list_for_stop_treak}")

            await client.send_message('@you_public_chenal_name', f"""✅Everything was deleted correctly, continued operation of element number {int(temporary_variable_to_receive)}""")

            exit()#Interrupting the compilation process to clear the cache

    except Exception as err:
        await client.send_message('@you_public_chenal_name', """Something went wrong, try again!❌""")

#Processing whether a variable is a string or a number №1------------------------------------------------------------------------------------------------------------------------------------------------------------------------

try :
    if list_with_forwards[1]['from'].isdigit() or list_with_forwards[1]['from'][0] == "-":
        output1_from = int(list_with_forwards[1]['from'])

    else :
        output1_from = list_with_forwards[1]['from']

    if list_with_forwards[1]['to'].isdigit() or list_with_forwards[1]['to'][0] == "-":
        output1_to = int(list_with_forwards[1]['to'])

    else :
        output1_to = list_with_forwards[1]['to']

    #Processing whether a variable is a string or a number №2------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[2]['from'].isdigit() or list_with_forwards[2]['from'][0] == "-":
        output2_from = int(list_with_forwards[2]['from'])

    else :
        output2_from = list_with_forwards[2]['from']

    if list_with_forwards[2]['to'].isdigit() or list_with_forwards[2]['to'][0] == "-":
        output2_to = int(list_with_forwards[2]['to'])

    else :
        output2_to = list_with_forwards[2]['to']

    #Processing whether a variable is a string or a number №3------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[3]['from'].isdigit() or list_with_forwards[3]['from'][0] == "-":
        output3_from = int(list_with_forwards[3]['from'])

    else :
        output3_from = list_with_forwards[3]['from']

    if list_with_forwards[3]['to'].isdigit() or list_with_forwards[3]['to'][0] == "-":
        output3_to = int(list_with_forwards[3]['to'])

    else :
        output3_to = list_with_forwards[3]['to']

    #Processing whether a variable is a string or a number №4------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[4]['from'].isdigit() or list_with_forwards[4]['from'][0] == "-":
        output4_from = int(list_with_forwards[4]['from'])

    else :
        output4_from = list_with_forwards[4]['from']

    if list_with_forwards[4]['to'].isdigit() or list_with_forwards[4]['to'][0] == "-":
        output4_to = int(list_with_forwards[4]['to'])

    else :
        output4_to = list_with_forwards[4]['to']

    #Processing whether a variable is a string or a number №5------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[5]['from'].isdigit() or list_with_forwards[5]['from'][0] == "-":
        output5_from = int(list_with_forwards[5]['from'])

    else :
        output5_from = list_with_forwards[5]['from']

    if list_with_forwards[5]['to'].isdigit() or list_with_forwards[5]['to'][0] == "-":
        output5_to = int(list_with_forwards[5]['to'])

    else :
        output5_to = list_with_forwards[5]['to']

    #Processing whether a variable is a string or a number №6------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[6]['from'].isdigit() or list_with_forwards[6]['from'][0] == "-":
        output6_from = int(list_with_forwards[6]['from'])

    else :
        output6_from = list_with_forwards[6]['from']

    if list_with_forwards[6]['to'].isdigit() or list_with_forwards[6]['to'][0] == "-":
        output6_to = int(list_with_forwards[6]['to'])

    else :
        output6_to = list_with_forwards[6]['to']

    #Processing whether a variable is a string or a number №7------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[7]['from'].isdigit() or list_with_forwards[7]['from'][0] == "-":
        output7_from = int(list_with_forwards[7]['from'])

    else :
        output7_from = list_with_forwards[7]['from']

    if list_with_forwards[7]['to'].isdigit() or list_with_forwards[7]['to'][0] == "-":
        output7_to = int(list_with_forwards[7]['to'])

    else :
        output7_to = list_with_forwards[7]['to']

    #Processing whether a variable is a string or a number №8------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[8]['from'].isdigit() or list_with_forwards[8]['from'][0] == "-":
        output8_from = int(list_with_forwards[8]['from'])

    else :
        output8_from = list_with_forwards[8]['from']

    if list_with_forwards[8]['to'].isdigit() or list_with_forwards[8]['to'][0] == "-":
        output8_to = int(list_with_forwards[8]['to'])

    else :
        output8_to = list_with_forwards[8]['to']

    #Processing whether a variable is a string or a number №9------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[9]['from'].isdigit() or list_with_forwards[9]['from'][0] == "-":
        output9_from = int(list_with_forwards[9]['from'])

    else :
        output9_from = list_with_forwards[9]['from']

    if list_with_forwards[9]['to'].isdigit() or list_with_forwards[9]['to'][0] == "-":
        output9_to = int(list_with_forwards[9]['to'])

    else :
        output9_to = list_with_forwards[9]['to']

    #Processing whether a variable is a string or a number №10------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[10]['from'].isdigit() or list_with_forwards[10]['from'][0] == "-":
        output10_from = int(list_with_forwards[10]['from'])

    else :
        output10_from = list_with_forwards[10]['from']

    if list_with_forwards[10]['to'].isdigit() or list_with_forwards[10]['to'][0] == "-":
        output10_to = int(list_with_forwards[10]['to'])

    else :
        output10_to = list_with_forwards[10]['to']

    #Processing whether a variable is a string or a number №11------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[11]['from'].isdigit() or list_with_forwards[11]['from'][0] == "-":
        output11_from = int(list_with_forwards[11]['from'])

    else :
        output11_from = list_with_forwards[11]['from']

    if list_with_forwards[11]['to'].isdigit() or list_with_forwards[11]['to'][0] == "-":
        output11_to = int(list_with_forwards[11]['to'])

    else :
        output11_to = list_with_forwards[11]['to']

    #Processing whether a variable is a string or a number №12------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[12]['from'].isdigit() or list_with_forwards[12]['from'][0] == "-":
        output12_from = int(list_with_forwards[12]['from'])

    else :
        output12_from = list_with_forwards[12]['from']

    if list_with_forwards[12]['to'].isdigit() or list_with_forwards[12]['to'][0] == "-":
        output12_to = int(list_with_forwards[12]['to'])

    else :
        output12_to = list_with_forwards[12]['to']

    #Processing whether a variable is a string or a number №13------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[13]['from'].isdigit() or list_with_forwards[13]['from'][0] == "-":
        output13_from = int(list_with_forwards[13]['from'])

    else :
        output13_from = list_with_forwards[13]['from']

    if list_with_forwards[13]['to'].isdigit() or list_with_forwards[13]['to'][0] == "-":
        output13_to = int(list_with_forwards[13]['to'])

    else :
        output13_to = list_with_forwards[13]['to']

    #Processing whether a variable is a string or a number №14------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[14]['from'].isdigit() or list_with_forwards[14]['from'][0] == "-":
        output14_from = int(list_with_forwards[14]['from'])

    else :
        output14_from = list_with_forwards[14]['from']

    if list_with_forwards[14]['to'].isdigit() or list_with_forwards[14]['to'][0] == "-":
        output14_to = int(list_with_forwards[14]['to'])

    else :
        output14_to = list_with_forwards[14]['to']

    #Processing whether a variable is a string or a number №15------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[15]['from'].isdigit() or list_with_forwards[15]['from'][0] == "-":
        output15_from = int(list_with_forwards[15]['from'])

    else :
        output15_from = list_with_forwards[15]['from']

    if list_with_forwards[15]['to'].isdigit() or list_with_forwards[15]['to'][0] == "-":
        output15_to = int(list_with_forwards[15]['to'])

    else :
        output15_to = list_with_forwards[15]['to']

    #Processing whether a variable is a string or a number №16------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[16]['from'].isdigit() or list_with_forwards[16]['from'][0] == "-":
        output16_from = int(list_with_forwards[16]['from'])

    else :
        output16_from = list_with_forwards[16]['from']

    if list_with_forwards[16]['to'].isdigit() or list_with_forwards[16]['to'][0] == "-":
        output16_to = int(list_with_forwards[16]['to'])

    else :
        output16_to = list_with_forwards[16]['to']

    #Processing whether a variable is a string or a number №17------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[17]['from'].isdigit() or list_with_forwards[17]['from'][0] == "-":
        output17_from = int(list_with_forwards[17]['from'])

    else :
        output17_from = list_with_forwards[17]['from']

    if list_with_forwards[17]['to'].isdigit() or list_with_forwards[17]['to'][0] == "-":
        output17_to = int(list_with_forwards[17]['to'])

    else :
        output17_to = list_with_forwards[17]['to']

    #Processing whether a variable is a string or a number №18------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[18]['from'].isdigit() or list_with_forwards[18]['from'][0] == "-":
        output18_from = int(list_with_forwards[18]['from'])

    else :
        output18_from = list_with_forwards[18]['from']

    if list_with_forwards[18]['to'].isdigit() or list_with_forwards[18]['to'][0] == "-":
        output18_to = int(list_with_forwards[18]['to'])

    else :
        output18_to = list_with_forwards[18]['to']

    #Processing whether a variable is a string or a number №19------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[19]['from'].isdigit() or list_with_forwards[19]['from'][0] == "-":
        output19_from = int(list_with_forwards[19]['from'])

    else :
        output19_from = list_with_forwards[19]['from']

    if list_with_forwards[19]['to'].isdigit() or list_with_forwards[19]['to'][0] == "-":
        output19_to = int(list_with_forwards[19]['to'])

    else :
        output19_to = list_with_forwards[19]['to']

    #Processing whether a variable is a string or a number №20------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if list_with_forwards[20]['from'].isdigit() or list_with_forwards[20]['from'][0] == "-":
        output20_from = int(list_with_forwards[20]['from'])

    else :
        output20_from = list_with_forwards[20]['from']

    if list_with_forwards[20]['to'].isdigit() or list_with_forwards[20]['to'][0] == "-":
        output20_to = int(list_with_forwards[20]['to'])

    else :
        output20_to = list_with_forwards[20]['to']

except Exception as err:

    chenge_numbers_in_main_dict = dict()#temporary variable to store data
    local_counter = int()#temporary variable to store data
    if counter == 0:
        counter+=1

    del list_with_forwards[int(counter)]

    for i in list_with_forwards:#Construction for correct replacement of a sequence of values occurs when an element is removed from the dict
        local_counter+=1
        chenge_numbers_in_main_dict[local_counter] = {}#Preliminary creation of an element in the dictionary
        chenge_numbers_in_main_dict[local_counter].update(list_with_forwards[i])#Adding an item to a dictionary

    counter-=1

    list_with_forwards = chenge_numbers_in_main_dict

    list_with_forwards[20] = {}#Pre-allocating memory in the dictionary to record values

    list_with_forwards[20].update({"from":"stubb", "to":"stubb"})#Adding a new element in place of the deleted one so that there are always 5 values
        
    with open("File_to_save_information_on_reboot.txt", "w") as file1:#Writing a dictionary update to a text file
        file1.write(f"{list_with_forwards}")

    with open("variable_storage_file.txt", "w") as file1:#Saving a count variable to a text file
        file1.write(f"{counter}")
    exit()#Interrupting the compilation process to clear the cache

#Forwarding messages №1-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if not 1 in list_for_stop_treak:
    @client.on(events.NewMessage(output1_from))
    async def forwarding1(event) -> None:

        global list_for_check_repetitions

        if not 1 in list_for_stop_treak:
            if len(list_with_forwards[1]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[1]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 
                                
                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 
                                
                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 
                                
                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet']) 

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 
                                

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[1]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 
                                
                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 
                                
                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 
                                
                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output1_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 1 in list_for_stop_treak:
                                list_for_stop_treak.append(1)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                                    file1.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""") 

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output1_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])
                    
                    if not 1 in list_for_stop_treak:
                        list_for_stop_treak.append(1)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                            file1.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""")
                        
                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output1_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])
                    
                    if not 1 in list_for_stop_treak:
                        list_for_stop_treak.append(1)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                            file1.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output1_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])
                
                    if not 1 in list_for_stop_treak:
                        list_for_stop_treak.append(1)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                            file1.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output1_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet']) 

                    if not 1 in list_for_stop_treak:
                        list_for_stop_treak.append(1)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file1:#Saving a sleep variable to a text file
                            file1.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 1”‼️""")
                    

#Forwarding messages №2-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 2 in list_for_stop_treak:
    @client.on(events.NewMessage(output2_from))
    async def forwarding2(event) -> None:

        global list_for_check_repetitions
        if not 2 in list_for_stop_treak:
            if len(list_with_forwards[2]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[2]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        
                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        
                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        
                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        
                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[2]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        
                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        
                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        
                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output2_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 2 in list_for_stop_treak:
                                list_for_stop_treak.append(2)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                                    file2.write(f"{list_for_stop_treak}")

                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                        

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output2_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 2 in list_for_stop_treak:
                        list_for_stop_treak.append(2)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                            file2.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                
                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output2_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 2 in list_for_stop_treak:
                        list_for_stop_treak.append(2)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                            file2.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                
                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output2_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 2 in list_for_stop_treak:
                        list_for_stop_treak.append(2)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                            file2.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                
                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output2_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 2 in list_for_stop_treak:
                        list_for_stop_treak.append(2)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file2:#Saving a sleep variable to a text file
                            file2.write(f"{list_for_stop_treak}")

                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 2”‼️""")
                    

#Forwarding messages №3-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 3 in list_for_stop_treak:
    @client.on(events.NewMessage(output3_from))
    async def forwarding3(event) -> None:

        global list_for_check_repetitions
        if not 3 in list_for_stop_treak:
            if len(list_with_forwards[3]) == 3:
                try:#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[3]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[3]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")


                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")


                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")


                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output3_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 3 in list_for_stop_treak:
                                list_for_stop_treak.append(3)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                                    file3.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")


            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output3_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])
                    
                    if not 3 in list_for_stop_treak:
                        list_for_stop_treak.append(3)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                            file3.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output3_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])
                    
                    if not 3 in list_for_stop_treak:
                        list_for_stop_treak.append(3)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                            file3.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output3_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])
                    
                    if not 3 in list_for_stop_treak:
                        list_for_stop_treak.append(3)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                            file3.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output3_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 3 in list_for_stop_treak:
                        list_for_stop_treak.append(3)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file3:#Saving a sleep variable to a text file
                            file3.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 3”‼️""")


#Forwarding messages №4-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 4 in list_for_stop_treak:
    @client.on(events.NewMessage(output4_from))
    async def forwarding4(event) -> None:

        global list_for_check_repetitions
        if not 4 in list_for_stop_treak:
            if len(list_with_forwards[4]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[4]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[4]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output4_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 4 in list_for_stop_treak:
                                list_for_stop_treak.append(4)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                                    file4.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output4_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 4 in list_for_stop_treak:
                        list_for_stop_treak.append(4)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                            file4.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output4_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 4 in list_for_stop_treak:
                        list_for_stop_treak.append(4)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                            file4.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output4_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 4 in list_for_stop_treak:
                        list_for_stop_treak.append(4)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                            file4.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output4_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 4 in list_for_stop_treak:
                        list_for_stop_treak.append(4)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file4:#Saving a sleep variable to a text file
                            file4.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 4”‼️""")


#Forwarding messages №5-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 5 in list_for_stop_treak:
    @client.on(events.NewMessage(output5_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions
        if not 5 in list_for_stop_treak:
            if len(list_with_forwards[5]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[5]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[5]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output5_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 5 in list_for_stop_treak:
                                list_for_stop_treak.append(5)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                                    file5.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output5_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 5 in list_for_stop_treak:
                        list_for_stop_treak.append(5)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                            file5.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output5_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 5 in list_for_stop_treak:
                        list_for_stop_treak.append(5)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                            file5.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output5_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 5 in list_for_stop_treak:
                        list_for_stop_treak.append(5)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                            file5.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output5_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 5 in list_for_stop_treak:
                        list_for_stop_treak.append(5)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file5:#Saving a sleep variable to a text file
                            file5.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 5”‼️""")

#Forwarding messages №6-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 6 in list_for_stop_treak:
    @client.on(events.NewMessage(output6_from))
    async def forwarding6(event) -> None:

        global list_for_check_repetitions

        if not 6 in list_for_stop_treak:
            if len(list_with_forwards[6]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[6]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[6]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output6_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 6 in list_for_stop_treak:
                                list_for_stop_treak.append(6)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                                    file6.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output6_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 6 in list_for_stop_treak:
                        list_for_stop_treak.append(6)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                            file6.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output6_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 6 in list_for_stop_treak:
                        list_for_stop_treak.append(6)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                            file6.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output6_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 6 in list_for_stop_treak:
                        list_for_stop_treak.append(6)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                            file6.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")


                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output6_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 6 in list_for_stop_treak:
                        list_for_stop_treak.append(6)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file6:#Saving a sleep variable to a text file
                            file6.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 6”‼️""")

#Forwarding messages №7-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 7 in list_for_stop_treak:
    @client.on(events.NewMessage(output7_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions
        if not 7 in list_for_stop_treak:
            if len(list_with_forwards[7]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[7]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[7]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output7_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 7 in list_for_stop_treak:
                                list_for_stop_treak.append(7)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                                    file7.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output7_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 7 in list_for_stop_treak:
                        list_for_stop_treak.append(7)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                            file7.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output7_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 7 in list_for_stop_treak:
                        list_for_stop_treak.append(7)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                            file7.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output7_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 7 in list_for_stop_treak:
                        list_for_stop_treak.append(7)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                            file7.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output7_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 7 in list_for_stop_treak:
                        list_for_stop_treak.append(7)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file7:#Saving a sleep variable to a text file
                            file7.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 7”‼️""")

#Forwarding messages №8-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 8 in list_for_stop_treak:
    @client.on(events.NewMessage(output8_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions
        if not 8 in list_for_stop_treak:
            if len(list_with_forwards[8]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[8]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[8]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output8_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 8 in list_for_stop_treak:
                                list_for_stop_treak.append(8)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                                    file8.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output8_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 8 in list_for_stop_treak:
                        list_for_stop_treak.append(8)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                            file8.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output8_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 8 in list_for_stop_treak:
                        list_for_stop_treak.append(8)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                            file8.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output8_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 8 in list_for_stop_treak:
                        list_for_stop_treak.append(8)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                            file8.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output8_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 8 in list_for_stop_treak:
                        list_for_stop_treak.append(8)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file8:#Saving a sleep variable to a text file
                            file8.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 8”‼️""")


#Forwarding messages №9-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 9 in list_for_stop_treak:
    @client.on(events.NewMessage(output9_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 9 in list_for_stop_treak:
            if len(list_with_forwards[9]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[9]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[9]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output9_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 9 in list_for_stop_treak:
                                list_for_stop_treak.append(9)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                                    file9.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output9_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 9 in list_for_stop_treak:
                        list_for_stop_treak.append(9)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                            file9.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")


                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output9_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 9 in list_for_stop_treak:
                        list_for_stop_treak.append(9)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                            file9.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")


                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output9_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 9 in list_for_stop_treak:
                        list_for_stop_treak.append(9)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                            file9.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")


                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output9_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 9 in list_for_stop_treak:
                        list_for_stop_treak.append(9)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file9:#Saving a sleep variable to a text file
                            file9.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 9”‼️""")

#Forwarding messages №10-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 10 in list_for_stop_treak:
    @client.on(events.NewMessage(output10_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 10 in list_for_stop_treak:
            if len(list_with_forwards[10]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[10]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[10]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output10_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 10 in list_for_stop_treak:
                                list_for_stop_treak.append(10)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                                    file10.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output10_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 10 in list_for_stop_treak:
                        list_for_stop_treak.append(10)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                            file10.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output10_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 10 in list_for_stop_treak:
                        list_for_stop_treak.append(10)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                            file10.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output10_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 10 in list_for_stop_treak:
                        list_for_stop_treak.append(10)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                            file10.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output10_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 10 in list_for_stop_treak:
                        list_for_stop_treak.append(10)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file10:#Saving a sleep variable to a text file
                            file10.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 10”‼️""")

#Forwarding messages №11-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 11 in list_for_stop_treak:
    @client.on(events.NewMessage(output11_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 11 in list_for_stop_treak:
            if len(list_with_forwards[11]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[11]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[11]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")


                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")


                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output11_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 11 in list_for_stop_treak:
                                list_for_stop_treak.append(11)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                                    file11.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output11_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 11 in list_for_stop_treak:
                        list_for_stop_treak.append(11)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                            file11.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output11_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 11 in list_for_stop_treak:
                        list_for_stop_treak.append(11)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                            file11.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output11_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 11 in list_for_stop_treak:
                        list_for_stop_treak.append(11)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                            file11.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output11_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 11 in list_for_stop_treak:
                        list_for_stop_treak.append(11)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file11:#Saving a sleep variable to a text file
                            file11.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 11”‼️""")

#Forwarding messages №12-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 12 in list_for_stop_treak:
    @client.on(events.NewMessage(output12_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 12 in list_for_stop_treak:
            if len(list_with_forwards[12]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[12]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[12]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output12_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 12 in list_for_stop_treak:
                                list_for_stop_treak.append(12)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                                    file12.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")
            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output12_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 12 in list_for_stop_treak:
                        list_for_stop_treak.append(12)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                            file12.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output12_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 12 in list_for_stop_treak:
                        list_for_stop_treak.append(12)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                            file12.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output12_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 12 in list_for_stop_treak:
                        list_for_stop_treak.append(12)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                            file12.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output12_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 12 in list_for_stop_treak:
                        list_for_stop_treak.append(12)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file12:#Saving a sleep variable to a text file
                            file12.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 12”‼️""")

#Forwarding messages №13-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 13 in list_for_stop_treak:
    @client.on(events.NewMessage(output13_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 13 in list_for_stop_treak:
            if len(list_with_forwards[13]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[13]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[13]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output13_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 13 in list_for_stop_treak:
                                list_for_stop_treak.append(13)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                                    file13.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output13_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 13 in list_for_stop_treak:
                        list_for_stop_treak.append(13)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                            file13.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output13_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 13 in list_for_stop_treak:
                        list_for_stop_treak.append(13)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                            file13.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output13_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 13 in list_for_stop_treak:
                        list_for_stop_treak.append(13)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                            file13.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output13_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 13 in list_for_stop_treak:
                        list_for_stop_treak.append(13)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file13:#Saving a sleep variable to a text file
                            file13.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 13”‼️""")

#Forwarding messages №14-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 14 in list_for_stop_treak:
    @client.on(events.NewMessage(output14_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 14 in list_for_stop_treak:
            if len(list_with_forwards[14]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[14]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[14]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output14_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 14 in list_for_stop_treak:
                                list_for_stop_treak.append(14)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                                    file14.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output14_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 14 in list_for_stop_treak:
                        list_for_stop_treak.append(14)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                            file14.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output14_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 14 in list_for_stop_treak:
                        list_for_stop_treak.append(14)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                            file14.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output14_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 14 in list_for_stop_treak:
                        list_for_stop_treak.append(14)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                            file14.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output14_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 14 in list_for_stop_treak:
                        list_for_stop_treak.append(14)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file14:#Saving a sleep variable to a text file
                            file14.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 14”‼️""")

#Forwarding messages №15-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 15 in list_for_stop_treak:
    @client.on(events.NewMessage(output15_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 15 in list_for_stop_treak:
            if len(list_with_forwards[15]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[15]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[15]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output15_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 15 in list_for_stop_treak:
                                list_for_stop_treak.append(15)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                                    file15.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output15_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 15 in list_for_stop_treak:
                        list_for_stop_treak.append(15)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                            file15.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output15_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 15 in list_for_stop_treak:
                        list_for_stop_treak.append(15)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                            file15.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output15_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 15 in list_for_stop_treak:
                        list_for_stop_treak.append(15)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                            file15.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output15_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 15 in list_for_stop_treak:
                        list_for_stop_treak.append(15)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file15:#Saving a sleep variable to a text file
                            file15.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 15”‼️""")

#Forwarding messages №16-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 16 in list_for_stop_treak:
    @client.on(events.NewMessage(output16_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions

        if not 16 in list_for_stop_treak:
            if len(list_with_forwards[16]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[16]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[16]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output16_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 16 in list_for_stop_treak:
                                list_for_stop_treak.append(16)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                                    file16.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output16_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 16 in list_for_stop_treak:
                        list_for_stop_treak.append(16)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                            file16.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output16_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 16 in list_for_stop_treak:
                        list_for_stop_treak.append(16)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                            file16.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output16_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 16 in list_for_stop_treak:
                        list_for_stop_treak.append(16)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                            file16.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output16_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 16 in list_for_stop_treak:
                        list_for_stop_treak.append(16)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file16:#Saving a sleep variable to a text file
                            file16.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 16”‼️""")

#Forwarding messages №17-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 17 in list_for_stop_treak:
    @client.on(events.NewMessage(output17_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions
        
        if not 17 in list_for_stop_treak:
            if len(list_with_forwards[17]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[17]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[17]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output17_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 17 in list_for_stop_treak:
                                list_for_stop_treak.append(17)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                                    file17.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output17_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 17 in list_for_stop_treak:
                        list_for_stop_treak.append(17)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                            file17.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output17_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 17 in list_for_stop_treak:
                        list_for_stop_treak.append(17)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                            file17.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output17_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 17 in list_for_stop_treak:
                        list_for_stop_treak.append(17)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                            file17.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output17_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 17 in list_for_stop_treak:
                        list_for_stop_treak.append(17)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file17:#Saving a sleep variable to a text file
                            file17.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 17”‼️""")

#Forwarding messages №18-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 18 in list_for_stop_treak:
    @client.on(events.NewMessage(output18_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions
        
        if not 18 in list_for_stop_treak:
            if len(list_with_forwards[18]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[18]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[18]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output18_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 18 in list_for_stop_treak:
                                list_for_stop_treak.append(18)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                                    file18.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output18_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 18 in list_for_stop_treak:
                        list_for_stop_treak.append(18)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                            file18.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output18_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 18 in list_for_stop_treak:
                        list_for_stop_treak.append(18)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                            file18.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output18_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 18 in list_for_stop_treak:
                        list_for_stop_treak.append(18)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                            file18.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output18_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 18 in list_for_stop_treak:
                        list_for_stop_treak.append(18)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file18:#Saving a sleep variable to a text file
                            file18.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 18”‼️""")

#Forwarding messages №19-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 19 in list_for_stop_treak:
    @client.on(events.NewMessage(output19_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions
        if not 19 in list_for_stop_treak:
            if len(list_with_forwards[19]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[19]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                                
                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                                
                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[19]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                                
                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                                
                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                                
                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output19_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 19 in list_for_stop_treak:
                                list_for_stop_treak.append(19)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                                    file19.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")

            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output19_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 19 in list_for_stop_treak:
                        list_for_stop_treak.append(19)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                            file19.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                        
                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output19_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 19 in list_for_stop_treak:
                        list_for_stop_treak.append(19)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                            file19.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                        
                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output19_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                    if not 19 in list_for_stop_treak:
                        list_for_stop_treak.append(19)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                            file19.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")
                        
                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output19_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 19 in list_for_stop_treak:
                        list_for_stop_treak.append(19)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file19:#Saving a sleep variable to a text file
                            file19.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 19”‼️""")

#Forwarding messages №20-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if not 20 in list_for_stop_treak:
    @client.on(events.NewMessage(output20_from))
    async def forwarding5(event) -> None:

        global list_for_check_repetitions
        
        if not 20 in list_for_stop_treak:
            if len(list_with_forwards[20]) == 3:
                try :#Handling receiving an address from a user from a channel
                    if str(event.from_id.user_id) in list_with_forwards[20]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                

                except Exception as err:#Processing pree_id for parsing from channels from the mini channel
                    if str(event.peer_id.channel_id) == list_with_forwards[20]['id']:
                        wallet_addresses, wallet_links = extract_wallet_addresses(event.text)
                        if len(list_for_check_repetitions) > 5:
                            list_for_check_repetitions = []

                        if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                

                        if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_addresses['Ethereum'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                

                        if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_addresses['Solana'][0]}""")

                            list_for_check_repetitions.append(wallet_addresses['Solana'][0])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                

                        if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                            await client.send_message(output20_to, f"""{wallet_links[0]['wallet']}""")

                            list_for_check_repetitions.append(wallet_links[0]['wallet'])

                            if not 20 in list_for_stop_treak:
                                list_for_stop_treak.append(20)

                                with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                                    file20.write(f"{list_for_stop_treak}")
                                    
                                await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
                
        
            else :
                wallet_addresses, wallet_links = extract_wallet_addresses(event.text)

                if len(list_for_check_repetitions) > 5:
                    list_for_check_repetitions = []

                if len(wallet_addresses['Bitcoin']) != 0 and not wallet_addresses['Bitcoin'][0] in list_for_check_repetitions:
                    await client.send_message(output20_to, f"""{wallet_addresses['Bitcoin'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Bitcoin'][0])

                    if not 20 in list_for_stop_treak:
                        list_for_stop_treak.append(20)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                            file20.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
        

                if len(wallet_addresses['Ethereum']) != 0 and not wallet_addresses['Ethereum'][0] in list_for_check_repetitions:
                    await client.send_message(output20_to, f"""{wallet_addresses['Ethereum'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Ethereum'][0])

                    if not 20 in list_for_stop_treak:
                        list_for_stop_treak.append(20)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                            file20.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
        

                if len(wallet_addresses['Solana']) != 0 and not wallet_addresses['Solana'][0] in list_for_check_repetitions:
                    await client.send_message(output20_to, f"""{wallet_addresses['Solana'][0]}""")

                    list_for_check_repetitions.append(wallet_addresses['Solana'][0])


                    if not 20 in list_for_stop_treak:
                        list_for_stop_treak.append(20)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                            file20.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")
        
                if len(wallet_links) != 0 and not wallet_links[0]['wallet'] in list_for_check_repetitions:
                    await client.send_message(output20_to, f"""{wallet_links[0]['wallet']}""")

                    list_for_check_repetitions.append(wallet_links[0]['wallet'])

                    if not 20 in list_for_stop_treak:
                        list_for_stop_treak.append(20)

                        with open("File_to_sleap_trecing_proces.txt", "w") as file20:#Saving a sleep variable to a text file
                            file20.write(f"{list_for_stop_treak}")
                            
                        await client.send_message('@you_public_chenal_name', """‼️The message has been forwarded and the contact is in sleep mode. in order to resume the forwarding operation, write the command “dell stop 20”‼️""")

client.run_until_disconnected()#Endless bot compilation
