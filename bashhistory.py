from collections import deque
import re

class BashHistory(deque):
	def __init__(self,HISTSIZE=500):
		self.HISTSIZE = HISTSIZE
		deque.__init__(self, maxlen=HISTSIZE)
	
	#TODO
#	Decide whether to return string or arg list, and more importantly what to store. 
#i think, store list, but return string	
# this could be called in precmd.  actually, we should probably store in
# history when hist_replace is called....
# :p would then return no_cmd, but would add to list

# 
	
	def history(self,N=15):
		"""show last N items"""
#		for i,s in enumerate(list(self)[-N:],len(self)-N):
		for i,s in zip(range(len(list(self))),list(self))[-N:]:
			print i,':',' '.join(s)
		try:
			i=int(raw_input(':'))
		except ValueError:
			i=-1
		try:
			print i, self[i]
			return ' '.join(self[i].replace(' ',"' '"))
		except:
			return '\n'

	def history_popup(self,N=15):
		try:
			import ui
		except ImportError:
			return self.history(N)
		v=ui.TableView()
		v.data_source=ui.ListDataSource( [' '.join([s.replace(' ',"' '") for s in x]) for x in list(self)[-N:]])
		v.delegate=v.data_source		
		v.height=v.row_height*N+10
		v.width=400
		v.data_source.autoresizing=True 
		def _rowselected(sender):
			sender.tableview.close()
		v.delegate.action=	_rowselected
		v.present('popover')
		v.wait_modal()
		print v.selected_row[1]+len(self)-min(len(self),N), ':',v.data_source.items[v.selected_row[1]]
		try:
			return v.data_source.items[v.selected_row[1]]
		except:
			return ''
			
	def history_replace(self, line):
		"""expand the following:
				!!	last command
				!$  last argument of last command
				!*	all of arguments of previous command
				!N	execute line N
				!-N execute line N ago
		===TODO not yet implemented===
				^STRING^string	replace STRING with string
				:p	print and add to history, but dont execute
		"""


# bleh, this regex will unintentionally match single !, so need to handle all None in process
		for m in re.finditer(r'!((?P<bang>!)|((?P<digits>-{0,1}\d*)(?P<char>[\*$]{0,1})))(?P<modifier>:p){0,1}',line):
			line=self._process_match(line,m)
		return line

	def _process_match(self,line,m):
		"""replace the bit in line with history expansion"""
		# if we got here, we are doing hist subst.  default line is previous, unless digits group exists
		# self contains parsed lists, i.e [cmd,arg1,arg2]
		c= m.groupdict()['char']
		d= m.groupdict()['digits']
		if not any(m.groupdict().itervalues()):
			return line
		else:
			histidx=-1	
			if d:
				histidx=int(d)
		
			start_arg=0
			if c:
				if c[0]==r'$':
					start_arg = -1
				elif c[0]==r'*':
					start_arg = 1
			try:
				hist=	self[histidx][start_arg:]
				return re.sub(re.escape(m.group(0)),' '.join(hist),line )
			except:
				return line


		#todo: handle modifiers

		
c=BashHistory()
[c.append([chr(ord('a')+i)*25]) for i in range(23)]

		
