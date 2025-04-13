import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="My Personal Library",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

LIBRARY_FILE = "library.json"

st.markdown("""
<style>
    .stApp {
        background-color: #0B0C10;
        color: #FFFFFF;
    }
    
   [data-testid="stSidebar"] {
    background-color: #0B0C10 !important;
    border-right: 1px solid #00C770 !important;
}
    
    h1 {
        color: #00C770;
        text-align: center;
        font-family: 'Georgia', serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 25px;
    }
    
    h2 {
        color: #00C770;
        border-bottom: 2px solid #00C770;
        padding-bottom: 8px;
        font-family: 'Georgia', serif;
    }
    
    h3 {
        color: #00C770;
        font-family: 'Georgia', serif;
    }
    
    .stButton>button {
        background-color: #00C770;
        color: #0B0C10;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #00A55A;
        color: #FFFFFF;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .book-card {
        background-color: #1A1D24;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        border-left: 5px solid #00C770;
        transition: all 0.3s;
    }
            .st-bo {
    color: #00a55a  !important;
}
    
    .book-card:hover {
        box-shadow: 0 8px 15px rgba(0,0,0,0.3);
        transform: translateY(-3px);
    }
    
    .status-read {
        display: inline-block;
        background-color: rgba(0, 199, 112, 0.2);
        color: #00C770;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
            .stFormSubmitButton>button {
    background-color: #00C770 !important;
    color: #0B0C10 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    transition: all 0.3s !important;
}

.stFormSubmitButton>button:hover {
    background-color: #00A55A !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
}
    
    .status-unread {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.2);
        color: #FFFFFF;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .stat-card {
        background-color: #1A1D24;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .stat-value {
        font-size: 1.9rem;
        font-weight: 600;
        margin: 10px 0;
        color: #00C770;
    }
    
    .stProgress>div>div>div {
        background-color: #00C770;
    }
    
   
    .st-cm {
    border-bottom-color: #00c770;
}

.st-cx {
    border-right-color: #00a55a;
}


.st-cw {
    border-left-color: #00a55a;
}
.st-cl {
    border-top-color: #00c770;
}

.st-ck {
    border-right-color: #00a55a;
}
.st-bd {
    background-color:#1A1D24;
}
            .st-cl {
    border-bottom-color: #00a55a;
}
     .st-emotion-cache-1iowko5 {
    color: rgb(240, 242, 246);
    background-color: #1A1D24;
}       

            .st-emotion-cache-1py5frv {

    border-style: solid;
    border-color: #00a55a;
   
}
        
input::placeholder,
textarea::placeholder {
    color: #fff !important;
    opacity: 0.7 !important;
}

.stTextInput input,
.stNumberInput input,
textarea {
    color: #FFFFFF !important; 
    background-color: #1A1D24 !important;
    border: 1px solid #00C770 !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

            .st-bo {
    color: rgb(213, 218, 229);
}
.st-cj {
    border-color: #00a55a;
}
    .stRadio>div>label {
        color: #FFFFFF !important;
    }
    
    .stCheckbox>label {
        color: #FFFFFF !important;
    }
            .st-fc {
    background-color: #00a55a;
}
    
   .stCheckbox input[type="checkbox"]:hover {
    border-color: #000000 !important; /* Change border color on hover */
}
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #00C770, transparent);
        margin: 25px 0;
    }
    
    .info-message {
        background-color: rgba(0, 199, 112, 0.1);
        border-left: 5px solid #00C770;
        padding: 18px;
        border-radius: 8px;
        margin: 20px 0;
        color: #FFFFFF;
    }
    
    .success-box {
        background-color: rgba(0, 199, 112, 0.1);
        border-left: 5px solid #00C770;
        padding: 18px;
        border-radius: 8px;
        margin: 20px 0;
        color: #FFFFFF;
    }
    
    .warning-box {
        background-color: rgba(255, 255, 255, 0.1);
        border-left: 5px solid #FFFFFF;
        padding: 18px;
        border-radius: 8px;
        margin: 20px 0;
        color: #FFFFFF;
    }
    
    .sidebar-header {
        color: #00C770;
        padding-bottom: 15px;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(0, 199, 112, 0.3);
        text-align: center;
    }
    
   .footer {
       
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #7F8C8D;
        font-size: 0.9rem;
        padding: 10px 0;
        background-color: #0B0C10;
        border-top: 1px solid #00C770;
        z-index: 100;
    }
    
    
    p {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

if 'library' not in st.session_state:
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            st.session_state.library = json.load(file)
    else:
        st.session_state.library = []

def save_library():
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(st.session_state.library, file, indent=4)

def add_book(title, author, year, genre, read_status):
    new_book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read_status,
        'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(new_book)
    save_library()
    st.markdown(f"""
    <div class="success-box">
        Book '{title}' added successfully!
    </div>
    """, unsafe_allow_html=True)

def remove_book(title):
    removed = False
    for book in st.session_state.library[:]:
        if book['title'].lower() == title.lower():
            st.session_state.library.remove(book)
            removed = True
    
    if removed:
        save_library()
        st.markdown(f"""
        <div class="success-box">
            Book '{title}' removed successfully!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Book '{title}' not found in the library.")

def search_books(search_term, search_by='title'):
    results = []
    for book in st.session_state.library:
        if search_term.lower() in book[search_by].lower():
            results.append(book)
    return results

def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read'])
    unread_books = total_books - read_books
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    genres = {}
    for book in st.session_state.library:
        genre = book['genre']
        genres[genre] = genres.get(genre, 0) + 1
    
    most_common_genre = max(genres.items(), key=lambda x: x[1])[0] if genres else "N/A"
    
    return {
        'total_books': total_books,
        'read_books': read_books,
        'unread_books': unread_books,
        'percentage_read': percentage_read,
        'most_common_genre': most_common_genre
    }

st.title("My Personal Library")

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2 style="color:#00C770; font-family: 'Georgia', serif;">Library Menu</h2>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigation",
        ["Home", "Add Book", "Remove Book", "Search Books", "Statistics"],
        label_visibility="collapsed"
    )

if menu == "Home":
    st.header("My Book Collection")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.markdown("""
        <div class="info-message">
            Your library is empty. Add some books to get started!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='color:#00C770; margin-bottom:25px;'>You have {len(st.session_state.library)} books in your collection</h3>", unsafe_allow_html=True)
        
        for book in st.session_state.library:
            read_status = "Read" if book['read'] else "Unread"
            status_class = "status-read" if book['read'] else "status-unread"
            
            with st.container():
                st.markdown(f"""
                <div class="book-card">
                    <h3 style="color:#00C770; margin-top:0;">{book['title']}</h3>
                    <p><b>Author:</b> {book['author']}</p>
                    <p><b>Year:</b> {book['year']} | <b>Genre:</b> {book['genre']}</p>
                    <div style="margin-top:12px;">
                        <span class="{status_class}">{read_status}</span>
                    </div>
                    <p style="margin-top:18px; font-size:0.85rem; color:#B0B0B0;">Added on: {book['date_added']}</p>
                </div>
                """, unsafe_allow_html=True)

elif menu == "Add Book":
    st.header("Add a New Book")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    with st.form("add_book_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title*", placeholder="Enter book title")
            author = st.text_input("Author*", placeholder="Enter author name")
            year = st.number_input("Publication Year*", min_value=1000, max_value=datetime.now().year)
        
        with col2:
            genre = st.selectbox(
                "Genre*",
                ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                 "Mystery", "Romance", "Biography", "History", "Other"]
            )
            read_status = st.checkbox("I have read this book")
        
        if st.form_submit_button("Add Book" ):
            if title and author:
                add_book(title, author, year, genre, read_status)
            else:
                st.error("Please fill in all required fields (marked with *)")

elif menu == "Remove Book":
    st.header("Remove a Book")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.markdown("""
        <div class="info-message">
            Your library is empty. There are no books to remove.
        </div>
        """, unsafe_allow_html=True)
    else:
        book_titles = [book['title'] for book in st.session_state.library]
        title_to_remove = st.selectbox("Select a book to remove", book_titles)
        
        if st.button("Remove Book", type="primary"):
            remove_book(title_to_remove)

elif menu == "Search Books":
    st.header("Search Books")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    search_by = st.radio(
        "Search by:",
        ["Title", "Author", "Genre"],
        horizontal=True
    )
    
    search_term = st.text_input(f"Enter {search_by.lower()} to search", placeholder="Enter book title or author...", key="search_input")
    
    if st.button("Search", type="primary"):
        if search_term:
            results = search_books(search_term, search_by.lower())
            if results:
                st.markdown(f"""
                <div class="success-box">
                    Found {len(results)} matching books
                </div>
                """, unsafe_allow_html=True)
                
                for book in results:
                    read_status = "Read" if book['read'] else "Unread"
                    status_class = "status-read" if book['read'] else "status-unread"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="book-card">
                            <h3 style="color:#00C770; margin-top:0;">{book['title']}</h3>
                            <p><b>Author:</b> {book['author']}</p>
                            <p><b>Year:</b> {book['year']} | <b>Genre:</b> {book['genre']}</p>
                            <div style="margin-top:12px;">
                                <span class="{status_class}">{read_status}</span>
                            </div>
                            <p style="margin-top:18px; font-size:0.85rem; color:#B0B0B0;">Added on: {book['date_added']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-box">
                    No books found matching your search.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-box">
                Please enter a search term.
            </div>
            """, unsafe_allow_html=True)

elif menu == "Statistics":
    st.header("Library Statistics")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.markdown("""
        <div class="info-message">
            Your library is empty. Add some books to see statistics.
        </div>
        """, unsafe_allow_html=True)
    else:
        stats = get_library_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h4>Total Books</h4>
                <div class="stat-value">{stats['total_books']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h4>Books Read</h4>
                <div class="stat-value">{stats['read_books']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <h4>Books Unread</h4>
                <div class="stat-value">{stats['unread_books']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stat-card">
            <h4>Reading Progress</h4>
        </div>
        """, unsafe_allow_html=True)
        st.progress(int(stats['percentage_read']))
        st.markdown(f"<p style='text-align:center; font-size:18px; margin-top:15px; color:#FFFFFF;'>{stats['percentage_read']:.1f}% of your books have been read</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <h4>Most Common Genre</h4>
            <div class="stat-value">{stats['most_common_genre']}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <p>My Personal Library App • Made by Neha Haneef</p>
</div>
""", unsafe_allow_html=True)
