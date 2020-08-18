import pysftp
import sys
import time

def pull_data():
	hname = "s-33fe515eee344b938.server.transfer.us-east-2.amazonaws.com"
	uname = "backtest_client"

	print("********** This Script fetches a file from the Greenwich SFTP server. **********")
	print("NOTE: Fetched files will be placed into current directory.")
	print("NOTE: RSA Private Key must placed in same directory as script.")
	print("The following files can be fetched:" + 
		"\n-> GHR_normalization.pdf" +
		"\n-> greenwich_master_backtestsamplepublic.manifest" +
		"\n-> greenwich_master_backtestsamplepublic.part_00000" +
		"\n-> greenwich_role_backtestsamplepublic.manifest" +
		"\n-> greenwich_role_backtestsamplepublic.part_00000" +
		"\n-> greenwich_tags_backtestsamplepublic.manifest" +
		"\n-> greenwich_tags_backtestsamplepublic.part_00000" +
		"\n-> greenwich_timelog_backtestsamplepublic.manifest" +
		"\n-> greenwich_timelog_backtestsamplepublic.part_00000" +
		"\n-> greenwich_titles_backtestsamplepublic.manifest" +
		"\n-> greenwich_titles_backtestsamplepublic.part_00000")
	print("File")

	file_name = input("Please enter file name to fetch from Greenwich server...")



	print('Attempting Server Connection...')
	try:
		server = pysftp.Connection(host = hname, username = uname, private_key = '/id_rsa_backtest_client.priv') #'./id_rsa_backtest_client.priv')
	except:
		print("Not able to establish Server connection")


	time.sleep(1)
	print("Fetching file: " + file_name + " from server.")
	try:
		server.get(file_name)
	except:
		print("Could not fetch file from server")


	time.sleep(1)
	print("***** Now closing connection to server.******* ")

	server.close()
	
	print(file_name + 'successfully saved in the directory')
