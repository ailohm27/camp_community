import streamlit as st

st.set_page_config(
    page_title="Start Page",
    page_icon="👋",
)
st.write("# IRE Design Automation POC")

st.sidebar.success("Select a page above.")

# Clears all data cached with st.cache_data
st.cache_data.clear()
# Clears all resources cached with st.cache_resource
st.cache_resource.clear()

st.markdown(
    """
    ## Introduction    
    This is the work of Alexis Lohman, Kaz Kazarnoff and Shanay Martin. 
    The purpose of this effort is to automate several key portions of AHEAD's delivery of our Isolated Recovery Environment (IRE) 
    Phase 1 service with the eventual intention of expanding this automation to all 3 phases and lay the ground-work for optimizing 
    project delivery processes organization-wide. 

   ## What's an IRE? 
    An Isolated Recovery Environment (IRE) is a highly secure, air-gapped system designed to protect critical backup 
    data and systems from cyber threats like ransomware, insider attacks, or accidental corruption. It operates as a 
    separate environment, disconnected from the primary network, ensuring that backup data remains safe even if the main 
    IT environment is compromised. Access to the IRE is heavily restricted, and data replication into the environment is 
    typically automated and conducted through secure, controlled mechanisms. This setup allows organizations to recover clean, 
    unaltered copies of their data during a disaster or security breach.   

    ## How AHEAD currently Delivers IREs
    At AHEAD, IREs are delivered in 3 phases over the course of 2-3 years, depending on a variety of factors. 

    ## Our Optimizations 
    The workstreams of this engagement followed the automation and templatization of the main deliverables provided at the end of an 
    IRE Phase 1: Design engagement.  

    An IRE Design Doc containing:  
    - IRE Cloud Architecture Diagrams  
    - IRE Network Architecture Diagrams  
    - IRE Backup Data Flow Diagrams  
    - IRE Security Pillars Determinations  

    Justifications for the choices made in each of the above:  
    - A RACI document indicating the level of Responsible, Accountable, Consulted, and Informed nature of each role highlighted as 
        necessary for the management and deployment of this environment.  
    - A SOW for Phase 2 generated from the output (deliverables) of Phase 1.  

    In that effort, the team focused on the creation of: 
        A domain ownership driven Client-facing Questionnaire (Microsoft Form) AND Delivery team ready templates (Excel) that serve as 
        data ingestion points for subsequent scripting and automation unique to the delivery needs of the engagement.
        Python scripts built to:  
             - Generate fake data   
             - Parse data from the questionnaire to create various diagrams  
         - The wireframe for Streamlit, used to create various architecture graphs from the client current and desired state inputs  
         - A RACI doc automatically populated with client's teams and roles as they related to domains covered in the IRE  
         - Instructions detailing how to use each piece of collateral to develop the desired deliverables.  

    ## Why it Matters 
    This culminates in a templatized deliverable package ready to be used and populated with the simple entry of several key datapoints. 
    Days if not weeks of works shortened to the span of hours to days, depending on client readiness.  

    One of our most recent IRE Phase 1 deals, a Discovery and Design for SMBC, is bringing AHEAD nearly \$1 million dollars in bookings 
    (\$941,530, to be exact) and is set to run from January of this year to January of next. If we're able to effectively halve (6 mo) 
    of even quarter (3mo)  the time taken for one of these engagements with our suggested automation and free those same delivery resources 
    to deliver more in the same time span, we'd be saving the client invaluable time and increasing the money in the AHEAD coffers by 
    millions, just on one project let alone across the inventory of IRE's we're currently delivering. We'll be able to make millions more 
    in the same time frame.  

    ## Future State
    The future-state with more time include:  
        Optimizations for each of the remaining phases.  
        Phase 1:  
        - Security Questionnaire section  
        - Cost Analysis section for new IRE environment  
        - Phase 2 and Phase 3 SOW development  
        Phase 2:  
        - Terraform code automation (based on chosen cloud)   
        Phase 3:  
        - Runbook automation  
        - Diagram creation automation  

    Other projects are going the way of automation. The true desired future state (at least at this point) is AHEAD automating as much of the delivery process of as many of its services as efficiently and quality controlled as possible.  

    But more importantly, and to answer  a question Cooper poised. "Can we use this now? Can we use this today?"  

    The answer resoundingly is YES.  

    There are optimizations to be made. There are ways to streamline this process, make it prettier, make the output a more detailed 
    representation of the environments they relate to and automate even more of the time consuming tasks delivery teams have to toll through.  

    But its current state today still helps us complete these tasks. We can still use this to create base backup data flow diagrams and network 
    architectures schemas that ATC or PTC resources can build upon without building from the ground up.  

    This still produces RACI templates in as long as it takes a client to fill a questionnaire a RACI template, that by myself took over a week 
    to iron out going back and forth with clients.  

    This still outlines an IRE Design doc that may have taken a PTC's entire afternoon or thanksgiving break (that happened) to draft.  

    Our solution starting today gives us time back on our calendars to do more of the work that keeps everyone's lights on.  

    I'll leave you with this. I checked PHX and we have a new Phase 1 Discover and Design engagement with SMBC that's slated to run from late 
    January of this year to January of next. The SOW wasn't on there for me to confirm, but lets imagine that it follows our standard delivery 
    framework for IREs, meaning the outcome would be the same deliverables that we've demoed for you today. That would mean, AHEAD would getting 
    paid close to a million dollars to produce those 5 documents in 12 months. With out solution, I don't think you'd need a full month per 
    document but lets say you do, and we shorten that engagement to 5 months.  

    And those same delivery resources are able to engage on another IRE this year. Possible even start a third by November/December. In the amount of time it would've taken us to produce 1 IRE and make about a million dollars, (\$941,530 to be exact) with our normal process and cadence, AHEAD stands to pocket twice that amount (\$1.9m) off delivered services, (the 2 phase 1's completed in 2025) sign/book 3 times that amount (SOW signed on 2 phase 2's and the Nov/Dec phase 1) (Savings would be \$300k per Phase 2. Savings would amount even greater, around \$900k for Nov/Dec, Phase 1). In total, that is an opportunity for \$3.4 million additional dollars that could be earned in various buckets but all in 2025 from ONE Phase 1 IRE implementing our solution. Right now we have over 9 IRE deals booked, 5 in the pipeline, and I don't even know how many still cooking. You do the math.  
"""
)