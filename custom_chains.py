from langchain import LLMChain
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain.chains import SequentialChain
from langchain.output_parsers import CommaSeparatedListOutputParser

from chain import get_chat_chain


def make_scriptWriteCritique_chain(verbose: str = False) -> LLMChain:

    #### TEMPLATES: ####
    # GENERATE SCRIPT TEMPLATE:
    generate_script_templates = []
    generate_script_templates.append(SystemMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        You write scripts for online orientation videos for colleges and universities.
        """))  # maybe add: (only include the script without directions)

    generate_script_templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=["video_topic", "institution_name"],
        template="""
        Write the {video_topic} video script for the school {institution_name}.
        """))

    generate_script_chain = get_chat_chain(
        templates=generate_script_templates, output_key="script", verbose=verbose)

    # CRITIQUE SCRIPT TEMPLATE:
    critique_script_templates = []
    critique_script_templates.append(SystemMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        You are a copywriter for online orientation videos for colleges and universities.
        """))
    critique_script_templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=["script"],
        template="""
        Critique this script:
        {script}

        """))
    # combined template:
    critique_script_chain = get_chat_chain(
        templates=critique_script_templates, output_key="critique", verbose=verbose)

    # EDIT SCRIPT TEMPLATE:
    edit_script_templates = []
    edit_script_templates.append(SystemMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        You are a copywriter for online orientation videos for colleges and universities. You are given a script and a list of critiques. You must edit the script to address the critiques.
        """))
    edit_script_templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=["script", "critique"],
        template="""
        Edit this script to address the following critiques:
        SCRIPT: {script}
        CRITIQUE: {critique}
        """))
    edit_script_chain = get_chat_chain(
        templates=edit_script_templates, output_key="edited_script", verbose=verbose)

    #### CREATE SEQUENTIAL CHAIN: ####
    chain = SequentialChain(
        chains=[generate_script_chain,
                critique_script_chain, edit_script_chain],
        input_variables=["video_topic", "institution_name"],
        output_variables=["script", "critique", "edited_script"],
        verbose=verbose
    )
    return chain


def make_parseOutline_chain(verbose: str = False) -> LLMChain:

    templates = []
    templates.append(SystemMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        You are given an unorganized outline of page titles, and you must format the titles into a list.
        Only include titles included in the outline.
        Format the list like this: "[pageName1, pageName2, pageNameN, ...]".
        You must only print the list of page titles in that format, and no other text.
        """))
    templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=[],
        template="Example input: Intro\nStudent Life\nAcademics"
    ))
    templates.append(AIMessagePromptTemplate.from_template(
        input_variables=[],
        template="[Intro, Student Life, Academics]"
    ))
    templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=["outline"],
        template="Input: {outline}",
        output_parser=CommaSeparatedListOutputParser()
    ))
    chain: LLMChain = get_chat_chain(
        templates=templates,
        output_key="page_titles",
        verbose=verbose)

    return chain


def make_pageContent_chain(verbose:str = False) -> LLMChain:
    
    templates = []
    templates.append(SystemMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        You are a copywriter for online orientation pages for colleges and universities.
        You are given a page title and you must write about the topic on the page in about 100-150 words.
        You are also given relevant information that you may use if it seems relevant.
        """))
    templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=["institution_name", "page_title", "relevant_info"],
        template="""
        Use this information if it seems relevant: {relevant_info}\n
        Write about the topic {page_title} for the school {institution_name}.
        """))
    chain = get_chat_chain(
        templates=templates,
        output_key="page_content",
        verbose=verbose)

    # chain = SequentialChain(
    #     chains=[chain],
    #     input_variables=["page_title", "relevant_info", "institution_name"],
    #     output_variables=["page_content"],
    #     verbose=True
    # )

    return chain

def make_findURLs_chain(verbose:str = False) -> LLMChain:

    templates = []
    templates.append(SystemMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        Your job is to extract all links/urls from the users text.
        Write them as a python list like this: ['url_1', 'url_2', ...]. 
        If there are none respond "NONE".
        DO NOT output any other text.
        """))
    templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        Example Input:\n
        TEXT:\n
        https://twu.edu/

        https://www.instagram.com/txwomans/?hl=en

        Do you have an online photo gallery for reference? (Example: Flickr, SmugMug, Photo Shelter, Google Drive, etc.)
        """
    ))
    templates.append(AIMessagePromptTemplate.from_template(
        input_variables=[],
        template="""['https://twu.edu/', 'https://www.instagram.com/txwomans/?hl=en']"""
    ))
    templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=[],
        template="""
        Example Input:\n
        TEXT:\n
        Mascot = Oakly the Owl. Use in orientation somewhere.  Likes their mascot and all campuses are familiar with the mascot.
        """
    ))
    templates.append(AIMessagePromptTemplate.from_template(
        input_variables=[],
        template="""NONE"""
    ))
    templates.append(HumanMessagePromptTemplate.from_template(
        input_variables=["text"],
        template="Input: {text}",
        output_parser=CommaSeparatedListOutputParser()
    ))
    chain: LLMChain = get_chat_chain(
        templates=templates,
        output_key="urls",
        verbose=verbose)

    return chain