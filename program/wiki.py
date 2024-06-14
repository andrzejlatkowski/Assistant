import wikipediaapi
from text_to_speach import play_audio

def get_wikipedia_page(search_term):
    wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')
    return wiki_wiki.page(search_term)


def speak_sections(page):
    titles = []
    excluded_sections = ["Sources", "External links", "See also"]

    def add_sections_with_text(sections):
        for section in sections:
            if section.title in excluded_sections:
                continue
            if section.text.strip():
                titles.append(section.title)
                add_sections_with_text(section.sections)
            else:
                add_sections_with_text(section.sections)

    add_sections_with_text(page.sections)
    print(', '.join(titles))
    return ', '.join(titles)

def read_wikipedia_section(page, section_title):
    possible_titles = [section_title.capitalize(), section_title.lower(), section_title.upper()]
    section = None
    for title in possible_titles:
        section = page.section_by_title(title)
        if section is not None:
            break
    if section is None:
        return f"The section title '{section_title}' was not found."
    print('\n' + section.text[:])
    return section.text[:]

# testing
# page = get_wikipedia_page('Computer science')
# sections_titles = speak_sections(page)
# play_audio(sections_titles)
# section_content = read_wikipedia_section(page, 'Artificial intelligence')
# play_audio(section_content)