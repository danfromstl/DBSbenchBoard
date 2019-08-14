
# Import critical modules
import requests
import json, pprint
from trello import TrelloClient

# this method is unused at the moment
client = TrelloClient(
    api_key='key',
    api_secret='secret',
    token='token',
    token_secret='secretToken'
)

def getMembersBoardsAndLists(memberId,memberApiKey,memberApiToken):
    """
    This function returns a dictionary of Trello Board Names
    
    (Only one API call)

    Arguments:
        
        memberId {string}
        memberApiKey {string}
        boardId {string} 
    """

    url = "https://api.trello.com/1/members/{}/boards".format(memberId)
    querystring = {"filter":"starred","fields":"name,id","lists":"open","memberships":"none","organization":"false","organization_fields":"name,displayName","key":memberApiKey,"token":memberApiToken}
    response = requests.request("GET", url, params=querystring)
    # pprint.pprint(response.text)

    boards_json = json.loads(response.content)
    board_dict = dict();
    board_dict['board_names'] = []
    board_dict['board_ids'] = []
    # board_dict['open_board_lists'] = {}


    for x in boards_json:
        board_dict['board_names'].append(x["name"])
        board_dict['board_ids'].append(x["id"])
    
    print('Board names and Ids pulled successfully! :-D')
    return(board_dict)


def pullListsFromBoard(boardId):
    """
    This function returns a dictionary of List IDs and Names

    Arguments:
        boardId {string} -- The ID of a board
    
    Returns:
        list_dict {dict} -- A dictionary of list IDs and names
    """

    url = "https://api.trello.com/1/boards/{}/lists".format(boardId)
    querystring = {"cards":"none","card_fields":"all","filter":"open","fields":"all","key":"46007e98096a244d3e1113d66641ebb0","token":"270e67673b1802abb66d06ab93f0a70c9d25734a74cd0787cbd615c6a8028212"}
    response = requests.request("GET", url, params=querystring)
    # print(response.text)
    dans_json = json.loads(response.content)
    list_dict = dict();
    list_dict['list_ids'] = []
    list_dict['list_names'] = []

    for x in dans_json:
        list_dict['list_ids'].append(x["id"])
        list_dict['list_names'].append(x["name"])
    return(list_dict)


def pullCardsFromList(single_list_id):
    """This function returns a list of carn names
    
    Arguments:
        single_list_id {string} -- a single list id
    
    Returns:
        card_names [list] -- a list of card name strings
    """

    url = "https://api.trello.com/1/lists/{}/cards?fields=id,name,badges,labels".format(single_list_id)
    querystring = {"fields":"name,closed,idBoard,pos","key":"46007e98096a244d3e1113d66641ebb0","token":"270e67673b1802abb66d06ab93f0a70c9d25734a74cd0787cbd615c6a8028212"}
    response = requests.request("GET", url, params=querystring)
    list_json = json.loads(response.content)
    card_names = []
    for card in list_json:
        card_names.append(card["name"])
    return card_names




############################
### BEGIN EXECUTION CODE ###
############################


dansMemberId = "id" # Dan's Member Id
dansAPIkey = "key" # BenchBoards's API key
dansAPItoken = "token" # BenchBoards's API key
globalAPIcalls = 0
boardAPIcalls = 0
listAPIcalls = 0
cardAPIcalls = 0

globalBoardDict = getMembersBoardsAndLists(dansMemberId,dansAPIkey,dansAPItoken)

globalAPIcalls += 1
boardAPIcalls += 1
# increment API calls for board GET



pprint.pprint(globalBoardDict)
# pretty print the board dictionary

print('---')
print('---')
print('---')

for eachBoard in globalBoardDict["board_ids"]:
    # for loop that runs through each board id in the board dictionary

    eachBoardLists = pullListsFromBoard(eachBoard) 
    # pull list names and ids then return to dict
    
    globalAPIcalls += 1
    listAPIcalls += 1
    # increment API calls by 1

    print(globalBoardDict["board_names"][globalBoardDict["board_ids"].index(eachBoard)] + ': There are {} lists on this board'.format(len(eachBoardLists["list_ids"])))
    # print the name of the board (from the 'globalBoardDict' dictionary) based on the index of the board_ids (also from the dictionary)
    # print the number of lists on the board (based on the length of the id list in the dictionary)

    print(eachBoardLists)
    print('-<><><>-')
    # print the board list dictionary and a spacer

    for eachList in eachBoardLists["list_ids"]:
            eachListCards = pullCardsFromList(eachList)
            #pull a list of card names based on a list id from the 'eachBoardList' dictionary

            globalAPIcalls += 1
            cardAPIcalls += 1
            # increment API calls by 1
            
            #### LINE TO ADAPT ###
            print(eachBoardLists["list_names"][eachBoardLists["list_ids"].index(eachList)] + ': (There are {} cards on this list)'.format(len(eachListCards)))
            # print the name of the list (from the 'eachBoardLists' dictionary) based on the index of the list id (also from the dictionary))
            # print the number of cards on a list (based on the length of the returned list)

            pprint.pprint(eachListCards)
            print('^v^v^')
            # pretty print the list of cards and print a spacer


print('---')
print('All lists printed successfully! :-D')
print('---')
print("Trello API called {} times".format(globalAPIcalls))
print("- {} times to get boards".format(boardAPIcalls))
print("- {} times to get lists".format(listAPIcalls))
print("- {} times to get cards".format(cardAPIcalls))


# globalListIdsDict = pullListsFromBoard("5d52f08135bef48f61e13f31")



