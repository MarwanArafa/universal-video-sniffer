from project import is_valid_url, get_extension, create_filename

def test_is_valid_url():
    # Test valid and invalid URLs
    assert is_valid_url("https://youtube.com") == True
    assert is_valid_url("http://google.com") == True
    assert is_valid_url("random text") == False

def test_get_extension():
    # Test user choices
    assert get_extension("1") == "mp4"
    assert get_extension("2") == "mp3"
    assert get_extension("3") == None
    assert get_extension("abc") == None

def test_create_filename():
    # Test filename cleaning
    assert create_filename("My Video", "mp4") == "My Video.mp4"
    assert create_filename("Video/with/bad/chars!", "mp3") == "Videowithbadchars.mp3"
    assert create_filename("Cool_Song-123", "mp4") == "Cool_Song-123.mp4"
