#importsection
import Tkinter
import tkFileDialog
import PIL
from PIL import Image,ImageTk
import Pmw,sys
import preprocess as pp

import cv2
import codecs
import initial_temp as it



#globalvariablesection
i=0

#classdefinition
class simpleapp(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent=parent
		self.source_url=Tkinter.StringVar()
		self.output_url=Tkinter.StringVar()
		self.current_url=Tkinter.StringVar()
		self.compare_url=Tkinter.StringVar()
		self.current_samp=Tkinter.StringVar()
		self.rec_char=Tkinter.StringVar()
		self.lines=[]
		

		self.draw_frame()
		self.initialize()



#initializefunction
	def initialize(self):

		#fuctiontoinitialize3urls
		self.load_default()
		self.draw_frame1()
		self.draw_frame2()
		self.draw_frame3()
		



	def load_default(self):
		self.current_samp.set(u'Default')
		self.source_url.set(u'Default/dc_books_page.png')
		self.output_url.set(u'Default/output_file.txt')
		self.load_lines()
		self.current_url.set(self.current_image_url())
		self.compare_url.set(u'Default/compare_list.txt')


	def draw_frame1(self):
		self.entry1=Tkinter.Entry(self.f1,textvariable=self.source_url)
		self.entry1.grid(column=0,row=0,sticky='EW')
		self.browse_button=Tkinter.Button(self.f1,text=u"Browse!",command=self.onBrowse1) #command=self.onBrowse1
		self.browse_button.grid(column=1,row=0)

		self.source_image=Image.open(self.source_url.get())
		self.source_image=self.source_image.resize((400,600),Image.ANTIALIAS)
		photo=ImageTk.PhotoImage(self.source_image)

		image_source=Tkinter.Label(self.f1,image=photo)
		image_source.image=photo
		image_source.grid(column=0,row=1,columnspan=2,sticky='NS')



	def draw_frame2(self):

		self.entry2=Tkinter.Entry(self.f2,textvariable=self.current_url)
		self.entry2.grid(column=0,row=0,sticky='EW')


		self.browse2_button=Tkinter.Button(self.f2,text=u"Browse!",command=self.onBrowse2)#,command=self.OnBrowse2
		self.browse2_button.grid(column=1,row=0)



		#fortheimage
		self.current_image=Image.open(self.current_url.get())
		image=self.current_image.resize((50,50),Image.ANTIALIAS)
		photo=ImageTk.PhotoImage(image)

		image_frame=Tkinter.Label(self.f2,image=photo)
		image_frame.image=photo
		image_frame.grid(column=0,row=1,columnspan=2,sticky='EW')


		#fortheforwardandreversebuttons
		self.next_button=Tkinter.Button(self.f2,text="Next",command=self.onNext)#,command=self.onNext
		self.prev_button=Tkinter.Button(self.f2,text="Previous",command=self.onPrevious)#,command=self.onPrevious
		self.next_button.grid(column=1,row=2,pady=5,padx=5)
		self.prev_button.grid(column=0,row=2,pady=5,padx=5)

		#forthetextsection
		
		self.rec_entry=Tkinter.Entry(self.f2,textvariable=self.rec_char,font='Calibri 44 bold',justify='center',width=6)
		#self.rec_entry.bind("<Return>",self.onEnter)
		self.rec_entry.grid(column=0,row=3)
		self.rec_char.set(self.current_rec_char())
		self.rec_entry.selection_range(0,Tkinter.END)
		#forsaveandeditbuttons

		self.edit_button=Tkinter.Button(self.f2,text="Edit",command=self.onEdit)#,command=self.onEdit

		self.save_button=Tkinter.Button(self.f2,text="Save",command=self.onSave)#,command=self.onSave

		self.edit_button.grid(column=0,row=4,pady=5,padx=5)

		self.save_button.grid(column=1,row=4,pady=5,padx=5)

		
		text=Pmw.ScrolledText(self.f2,borderframe=5,vscrollmode='none',hscrollmode='none'
		,labelpos='n',label_text='file  ALPHABETS',text_width=60,text_height=20)
		text.grid(row=6,column=0,sticky='EW')

		text.insert('end',open(str('./alphabet.txt'),'r').read())


	def draw_frame3(self):

		self.preview_button=Tkinter.Button(self.f3,text="Generate Preview",command=self.onPreview)

		self.preview_button.grid(column=0,row=0,sticky='EW',padx=5,pady=5)

		text=Pmw.ScrolledText(self.f3,borderframe=5,vscrollmode='dynamic',hscrollmode='dynamic'
		,labelpos='n',label_text='file  %s'%self.output_url.get(),text_width=60,text_height=40,text_wrap='none')
		text.grid(row=1,column=0,sticky='EW')

		text.insert('end',open(str(self.output_url.get()),'r').read())

	def draw_frame(self):
		self.f=Tkinter.Frame(self,bg="orange",width=800,height=500)
		self.f.pack(side=Tkinter.LEFT,expand=2,fill=Tkinter.BOTH)

		self.f1=Tkinter.Frame(self.f,bg="red",width=500,height=500)
		self.f1.grid(column=0,row=0,padx=5,pady=5,sticky='EW')

		self.f2=Tkinter.Frame(self.f,bg="red",width=500,height=500)
		self.f2.grid(column=1,row=0,padx=5,pady=5)

		self.f3=Tkinter.Frame(self.f,bg="red",width=500,height=500)
		self.f3.grid(column=2,row=0,padx=5,pady=5,sticky='EW')



	def current_image_url(self):
		global i
		return self.current_samp.get()+'/samp/'+str(i)+'.png'

	def current_rec_char(self):
		global i
		print i
		if (self.lines[i][-1] =='\n'):
			self.lines[i]=self.lines[i][:-1]
		return self.lines[i]

	def load_lines(self):
		print self.current_samp.get()
		inp=open(self.current_samp.get()+'/compare_list.txt','r')
		self.lines=inp.readlines()

	def onNext(self):
		global i
		i+=1
		self.current_url.set(self.current_samp.get()+'/samp/'+str(i)+'.png')
		self.draw_frame2()

	def onPrevious(self):
		global i
		i=i-1
		# self.onChange()
		# print i
		if(i<0):
		    i=0
		# print self.current_url.get()
		self.current_url.set(self.current_samp.get()+'/samp/'+str(i)+'.png')
		self.draw_frame2()

	def onEdit(self):
		global i
		# self.rec_char.set( self.rec_char.get() )
		print self.rec_char.get().encode('utf8')
		self.lines[i]=self.rec_char.get().encode('utf8')
		self.draw_frame2()

	def onSave(self):
        
		inp=open(self.compare_url.get(),'w')
		for i in range(len(self.lines)):
		    if(self.lines[i][-1]=='\n'):
		        self.lines[i]=self.lines[i][:-1]
		    inp.write(self.lines[i]+'\n')
		inp.close()
		self.draw_frame2()

	def onPreview(self):
		f=open(self.compare_url.get(),'r')
		g=open(self.output_url.get(),'w')
		img=cv2.imread(self.source_url.get(),0)
		if(img==None):
		    print url+' does\'nt exist'
		    exit()
		img = pp.preprocess(img)
		im,rot = pp.skew_correction(img)
		line = pp.find_lines(im.copy())
		# print len(linene)
		label_list=it.train.label_unicode()
		q=f.readlines()
		i=0
		num=[]
		for l in line:
		    for w in l.word_list:
		        for c in w.char_list:
		           
		            tup=label_list[int(c.label)]
		            if(q[i][:-1]!=tup):
		                tup=q[i][:-1]
		           
		            g.write(tup)
		           
		            i+=1
		        g.write(' ')
		    g.write('\n')
		f.close()
		g.close()
		
		self.draw_frame3()

	def onBrowse1(self):
		# print "you clicked"
		self.source_url.set(tkFileDialog.askopenfilename())
		print self.source_url.get()
		self.draw_frame1()

	def onBrowse2(self):
		self.current_url.set(tkFileDialog.askopenfilename())
		print self.current_url.get()
		self.find_i_from_url()
		self.draw_frame2()
		self.draw_frame3()

	def find_i_from_url(self):
		list1=self.current_url.get().split('/')
		global i
		i= int(list1[-1][:-4])
		self.current_samp.set("/".join(list1[:-2]))
		self.compare_url.set( "/".join(list1[:-2])+'/compare_list.txt')
		self.output_url.set( "/".join(list1[:-2])+'/output_file.txt')
		self.load_lines()

if __name__=="__main__":
	app=simpleapp(None)
	app.title('MyApp')
	app.mainloop()


