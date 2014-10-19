#sally
from Yowsup.connectionmanager import YowsupConnectionManager
import json,base64,threading,time,urllib,HTMLParser,random
res = json.loads(open("res.json").read())
class MainBot():
	def __init__(self,user,passwd,res):
		self.con = YowsupConnectionManager()
		self.con.setAutoPong(True)
		self.res = res
		self.signalsInterface = self.con.getSignalsInterface()
		self.methodsInterface = self.con.getMethodsInterface()
		self.signalsInterface.registerListener("message_received", self.onMessageReceived)
		self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
		self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
		self.signalsInterface.registerListener("disconnected", self.onDisconnected)
		self.signalsInterface.registerListener("receipt_messageDelivered", self.onMessageDelivered)
		self.methodsInterface.call("auth_login", (user, base64.b64decode(passwd)))
		self.running = True
		self.victims=[]
		self.threads_=[]

	def onAuthSuccess(self,args):
		print("Auth True")
		self.methodsInterface.call("ready")

	def onAuthFailed(self,args):
		print("Auth False")
		self.running = False

	def onDisconnected(self,args):
		print("Connection Terminated")
		self.running = False

	def onMessageDelivered(self,jid,messageId):
		print("Message Delivered")

	def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
		if not(jid in self.victims):
			self.victims.append(jid)
			haunt_ = threading.Thread(target=self.haunt,args=(jid,))
			print "------------>haunt" + str(jid)
			self.threads_.append(haunt_)
			haunt_.start()
			
		time.sleep(0.2)
		self.methodsInterface.call("message_ack", (jid, messageId))
		time.sleep(0.2)
		self.react(jid,messageContent)

	def react(self,jid,messageContent):
		messageContent = messageContent.upper()
		text = messageContent.split()	
		ch = lambda x:x in text
		if ch('HI') or ch('SUP') or ch('HELLO'):
			self.methodsInterface.call("message_send", (jid, "Hello, it's me Sally"))
		elif ch('LOL') or ch('BYE'):
			self.methodsInterface.call("message_send", (jid, text[0] + " and btw, die in hell"))
		elif ch('WHO') and ch('ARE'):
			self.methodsInterface.call("message_send", (jid, "dont envy me, you know who i am"))
		elif (ch("SEXY")):
			self.methodsInterface.call("message_send", (jid, "intrested in me, hah meet me at the 4th floor"))
		else:
			self.methodsInterface.call("message_send", (jid, self.random_m().encode('utf-8')))

	def random_m(self):
		return self.res["random"][random.randrange(0,len(self.res["random"]))]
	def repeater(self):
		cur = self.res["repeaters"][random.randrange(0,len(self.res["repeaters"]))]
		build=""
		for i in range(1,random.randrange(1,15)):
			exl = ""
			for x in range(0,i):
				exl +="!"
			build += " "+cur+" "+exl
		return build

	def haunt(self,jid):
		while True:
			time.sleep(60*60)
			if random.randrange(0,2) == 0:
				self.methodsInterface.call("message_send", (jid, self.random_m().encode('utf-8')))
			else:
				self.methodsInterface.call("message_send", (jid, self.repeater().encode('utf-8')))
			


raw_credentials = open('login.json').read()
credentials = json.loads(raw_credentials)
mb = MainBot(credentials["phone"],credentials["password"],res)

while True:
        if not mb.running:
        	time.sleep(1)
        	mb = None
        	mb = MainBot(credentials["phone"],credentials["password"],res)
