# UI
shinyUI(fluidPage(
  
  
  # Format
  tags$head(tags$style(
    'body {font-family:Palatino; font-size:16px;}')),
  
  # Banner
  br(),
  fluidRow(
    h1("DATA SCIENCE CAREER INSIGHTS",
       style='font-size:50px;font-weight:bold;text-align: center;color:#385280'),           
    column(10,h4(HTML('As a wanna-be Data Scientist, I often find myself overwhelmed by the bulk of knowledge and always-changing nature of this industry. 
                Thus, I was intrigued to figure out what exactly people in Data Science do and what it takes to become one, 
                so I decided to do a bit scraping of Data Science job posting data on LinkedIn in the hope of discovering some light at the end of the tunnel.
                Before you start, here are some <strong>FUN FACTS</strong> about my dataset')),
                style = 'text-align:center; padding-left:200px; line-height:2.5;')
    ),
  d3Output("d3"),
  
  
  # Inputs
    h2("Start your exploration here",   
       style='font-size:40px; text-align:center; color:black; margin-left:100px; margin-right:120px; 
              padding-top: 5px; padding-bottom:5px; background-color:#C3D2EC'),
    br(),
    fluidRow(
    column(3,selectInput(inputId = "title",label = "Select desired position",
                         choices = c("Big Data Developer","Consultant","Data Analyst","Data Engineer",
                                     "Data Scientist","Machine Learning Engineer"),
                         selected = "Data Scientist",
                         multiple = FALSE), offset = 3),
    column(4,checkboxGroupInput(inputId = "explevel", label = "Select experience level",
                                choices = c("Entry level","Associate","Senior"),
                                selected = 'Entry level',inline = TRUE))
  ),

  # Quick insights
  br(),
  wellPanel(
    h4("Quick Insights",style='font-size:30px; font-weight:bold; text-align:left; color:#385280; padding-left:30px;'),
    #br(),
    uiOutput("insight"),
    style = 'margin-left:100px; margin-right:100px; background-color:whitesmoke; border-radius:40px;'),
  
  
  # Tab sections
  hr(style = 'border-width:10px;'),  
  
  tags$style(HTML("
    .tabbable > ul > li > a {background-color: white;  border-color:darkblue; color:#385280; padding-left:50px; padding-right:100px}
    .tabbable > ul > li[class=active]    > a {background-color: #385280; color:white}
                  ")),
  
  div(
    tabsetPanel(
    tabPanel("Job Postings", icon = icon('briefcase'),
               tags$br(),
               wellPanel(selectInput(inputId = "country", label = "Select countries",
                                  choices = c("Australia","Canada","China","France","Germany",
                                              "India","Italy","Japan","Netherlands","Singapore",
                                              "South Africa","Spain","Sweden","Switzerland",
                                              "United Kingdom","United States"),
                                  selected = "Australia",multiple = TRUE),
                         style = 'width:80%; background-color:white; border-color:white'),
               tags$br(),
               uiOutput("listing")
      ),
    tabPanel("Roles & Skills", icon = icon("clipboard-check"),
            h3(textOutput('tit1'),style='font-size:22px;font-weight:bold'),
            helpText('Click a word to zoom in the corresponding branches. If there is an error message, simply refresh the page.',style='font-size:14px;font-style:italic'),
            gwordtree::gwordtreeOutput("wordtree", height = '200%', width = '200%'),
            h3(textOutput('tit2'),style='font-size:22px;font-weight:bold'),
            wellPanel(
              sliderInput(inputId = 'maxword',label = 'Select maximum number of words to display',
                             min = 1, max = 200, value = 100, step = 2),
              style = 'width:65%'),
            plotOutput('wordcloud',height = "450px", width = "80%")
    ),
    tabPanel("Education & Experience", icon = icon('book'),
             verticalLayout(
               h3('Minimum Years of Experience Required',style='font-size:22px;font-weight:bold'),
               plotOutput('stackedbar2'),
               h3('Requirements based on Experience Levels',style='font-size:22px;font-weight:bold'),
               radioButtons(inputId = "average", label = "Average Years of Experience by",
                                  choices = c('Mean','Median'), selected = 'Mean', inline = TRUE),
               plotlyOutput('combchart')
              )
    ),
    tabPanel("Job Demand", icon = icon('globe'), 
             h3('Potential Regions for Job Opportunities',style='font-size:22px;font-weight:bold;'),
             helpText('Left click to move to smaller areas',style='font-size:14px;font-style:italic;'),
             helpText('Right click to return to bigger areas (applicable for view on browser or new window)',style='font-size:14px;font-style:italic;'),
             htmlOutput("treemap"),
             h3('Potential Industries for Job Opportunities',style='font-size:22px;font-weight:bold'),
             helpText('Brush over an area to zoom in on the bars',style='font-size:14px;font-style:italic'),
             sliderInput(inputId = 'maxind',label = 'Show top industries',
                         min = 20, max = 123, value = 5, step = 1),
             plotlyOutput('bar')
    ),
    type = "pills"),
  style = 'padding-left:100px'
  
  )

)
)

