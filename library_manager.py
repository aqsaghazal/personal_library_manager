import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Custom font and colors */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #1E3D59;
        font-weight: 700 !important;
        padding-bottom: 1rem !important;
        border-bottom: 2px solid #E8E8E8;
        margin-bottom: 2rem !important;
    }
    
    h2 {
        color: #1E3D59;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #1E3D59;
        font-weight: 500 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #F5F7F9;
        padding: 2rem 1rem;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B6B;
        box-shadow: 0 0 0 2px rgba(255,107,107,0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Delete button */
    .delete-btn {
        background-color: #FF4B4B !important;
        padding: 0.3rem 0.8rem !important;
        font-size: 0.8rem !important;
    }
    
    /* Book cards */
    .book-card {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #E0E0E0;
        transition: all 0.3s ease;
    }
    
    .book-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Status badges */
    .status-read {
        background-color: #4CAF50;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    .status-unread {
        background-color: #FFA726;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    /* Metrics */
    .css-1r6slb0 {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Charts */
    .css-1v0mbdj {
        border-radius: 10px;
        padding: 1rem;
        background-color: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        color: #1E3D59;
        font-size: 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF6B6B !important;
        color: white !important;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border-color: #E8E8E8;
    }
    
    /* Search box */
    .search-box {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'library' not in st.session_state:
    if os.path.exists('library.txt'):
        with open('library.txt', 'r') as f:
            st.session_state.library = json.load(f)
    else:
        st.session_state.library = []

def save_library():
    """Save library to file"""
    with open('library.txt', 'w') as f:
        json.dump(st.session_state.library, f)

def add_book(title, author, year, genre, read_status):
    """Add a new book to the library"""
    book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    return True

def remove_book(index):
    """Remove a book from the library"""
    st.session_state.library.pop(index)
    save_library()

def get_statistics():
    """Calculate library statistics"""
    total_books = len(st.session_state.library)
    if total_books == 0:
        return {
            'total_books': 0,
            'read_books': 0,
            'unread_books': 0,
            'percent_read': 0,
            'genres': {}
        }
    
    read_books = sum(1 for book in st.session_state.library if book['read'])
    genres = {}
    for book in st.session_state.library:
        genres[book['genre']] = genres.get(book['genre'], 0) + 1
    
    return {
        'total_books': total_books,
        'read_books': read_books,
        'unread_books': total_books - read_books,
        'percent_read': (read_books / total_books) * 100,
        'genres': genres
    }

# Streamlit UI
st.title("📚 Personal Library Manager")

# Sidebar for adding books
with st.sidebar:
    st.header("Add New Book")
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=2024)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Have you read this book?")
        
        submitted = st.form_submit_button("Add Book")
        if submitted and title and author and genre:
            add_book(title, author, year, genre, read_status)
            st.success("Book added successfully!")
        elif submitted:
            st.error("Please fill in all fields!")

# Main content area
tab1, tab2, tab3 = st.tabs(["📚 Library", "🔍 Search", "📊 Statistics"])

with tab1:
    st.header("Your Library")
    if st.session_state.library:
        for index, book in enumerate(st.session_state.library):
            st.markdown(f"""
            <div class="book-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0;">{book['title']}</h3>
                        <p style="margin: 0.5rem 0; color: #666;">by {book['author']} ({book['year']})</p>
                        <p style="margin: 0; color: #888;">Genre: {book['genre']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span class="{'status-read' if book['read'] else 'status-unread'}">
                            {'Read' if book['read'] else 'Unread'}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Delete button
            if st.button('Delete', key=f'del_{index}', help="Remove this book"):
                remove_book(index)
                st.rerun()
    else:
        st.info("Your library is empty. Add some books!")

with tab2:
    st.header("Search Books")
    with st.container():
        st.markdown('<div class="search-box">', unsafe_allow_html=True)
        search_term = st.text_input("Search by title or author", placeholder="Enter search term...").lower()
        st.markdown('</div>', unsafe_allow_html=True)
        
        if search_term:
            results = [book for book in st.session_state.library 
                      if search_term in book['title'].lower() 
                      or search_term in book['author'].lower()]
            if results:
                for book in results:
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{book['title']}</h3>
                        <p>by {book['author']} ({book['year']})</p>
                        <p>Genre: {book['genre']}</p>
                        <span class="{'status-read' if book['read'] else 'status-unread'}">
                            {'Read' if book['read'] else 'Unread'}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No matching books found.")

with tab3:
    st.header("Library Statistics")
    stats = get_statistics()
    
    # Display key metrics in styled containers
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background-color: #F8F9FA; padding: 1rem; border-radius: 10px; text-align: center;">
            <h4 style="color: #1E3D59; margin: 0;">Total Books</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #FF6B6B; margin: 0.5rem 0;">
                {}</p>
        </div>
        """.format(stats['total_books']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #F8F9FA; padding: 1rem; border-radius: 10px; text-align: center;">
            <h4 style="color: #1E3D59; margin: 0;">Read Books</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #4CAF50; margin: 0.5rem 0;">
                {}</p>
        </div>
        """.format(stats['read_books']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #F8F9FA; padding: 1rem; border-radius: 10px; text-align: center;">
            <h4 style="color: #1E3D59; margin: 0;">Completion Rate</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #FF6B6B; margin: 0.5rem 0;">
                {:.1f}%</p>
        </div>
        """.format(stats['percent_read']), unsafe_allow_html=True)
    
    # Genre distribution
    if stats['genres']:
        st.subheader("Genre Distribution")
        genre_df = pd.DataFrame(list(stats['genres'].items()), columns=['Genre', 'Count'])
        st.bar_chart(genre_df.set_index('Genre'))
    
    # Reading progress over time
    if st.session_state.library:
        st.subheader("Reading Progress")
        timeline_df = pd.DataFrame(st.session_state.library)
        timeline_df['added_date'] = pd.to_datetime(timeline_df['added_date'])
        timeline_df = timeline_df.sort_values('added_date')
        timeline_df['cumulative_books'] = range(1, len(timeline_df) + 1)
        st.line_chart(timeline_df.set_index('added_date')['cumulative_books'])
