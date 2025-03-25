import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def compare(med_name):
    # this is for search 
  params = { 
  "engine": "google_shopping",
  "q": med_name,                     # q is here a searching different things
  "api_key": "e76edd93d1d2e20981577a0b2cb50df5b080e731445de990043bf7e172f6e464",
  "gl":"in"
}

  search = serpapi.GoogleSearch(params)
  results=search.get_dict()
  shopping_results=results["shopping_results"]   
  return shopping_results
  
# defining columns needed 
col1,col2=st.columns(2)
col1.image('e_pharmacy.png',width=200)
col2.header("E_Pharmacy Price Comparison System")

# sidebar creating
st.sidebar.title("Enter name of medicine")
med_name=st.sidebar.text_input('Enter Name here 👉')
number=st.sidebar.text_input('Enter Number Of Options Here 👉')

medicine_comp=[]
med_price=[]

# for searching and price comparison 
if med_name is not None:
    if st.sidebar.button("Price Compare"):
        shopping_results=compare(med_name)
        
        # consider a lowest price to compare to other price to remove dolor sign
        lowest_price=float(shopping_results[0].get('price')[1:])
        lowest_price_index=0
        
        # for image 
        st.sidebar.image(shopping_results[0].get('thumbnail'))    # 0 is here for image
        for elements in range(int(number)):
            current_price=float(shopping_results[elements].get('price')[1:])
            
            # company name and price
            medicine_comp.append(shopping_results[elements].get('source'))
            med_price.append(float(shopping_results[elements].get('price')[1:]))
            
            #----------------------------------------------- options---------
            st.title(f'Option{elements+1}')
            c1,c2=st.columns(2)
            c1.write('Company Name :')
            c2.write(shopping_results[elements].get('source'))
            
            c1.write('Title :')
            c2.write(shopping_results[elements].get('title'))
            
            c1.write('Price :')
            c2.write(shopping_results[elements].get('price'))
            
            url=shopping_results[elements].get('product_link') # link created
            c1.write('Buy link :')
            c2.write("[Link](%s)"%url)
            
            """__________________________________________________________"""  # to create line
            # comparison here
            if current_price<lowest_price:
                lowest_price=current_price
                lowest_price_index=elements
        
        # best option 
        st.title('Best Option : ')
        c1,c2=st.columns(2)
        c1.write('Company Name :')
        c2.write(shopping_results[lowest_price_index].get('source'))
            
        c1.write('Title :')
        c2.write(shopping_results[lowest_price_index].get('title'))
            
        c1.write('Price :')
        c2.write(shopping_results[lowest_price_index].get('price'))
            
        url=shopping_results[lowest_price_index].get('product_link') # link created to buy
        c1.write('Buy link :')
        c2.write("[Link](%s)"%url) 
        
        
        # graphs compare price and name
        df=pd.DataFrame(med_price,medicine_comp) 
        st.title('Chart comparison :')
        st.bar_chart(df)    
        
        # pie chart for comparison of product with price
        fig,ax=plt.subplots()
        ax.pie(med_price,labels=medicine_comp)  
        ax.axis('Equal')
        st.pyplot(fig)
