# By default, the googleVis plot command will open a browser window 
# and requires Internet connection to display the visualisation

library(shiny)
require(googleVis)
require(gwordtree)
#devtools::install_github("czxa/gwordtree")
library(wordcloud)
library(RColorBrewer)
require(ggplot2)
require(plotly)
require(r2d3)


# Load datatsets
data1 = read.csv('data1.csv',stringsAsFactors = FALSE)
data2 = read.csv('data2.csv')
data3 = read.csv('data3.csv')
data4 = read.csv('data4.csv')
data5 = read.csv('data5.csv', stringsAsFactors = FALSE)

# Sort levels of exp level
data4$exp_level_v3 = factor(data4$exp_level_v3, levels = c('Entry level','Associate','Senior'))
# Sort levels of min degree
data4$min_degree = factor(data4$min_degree, levels = c('Bachelor','Master','Phd','Not Required'))


# Intialize user options
position = levels(data4$title_v3) # data position
exp_level = levels(data4$exp_level_v3) # experience level
country = levels(data4$country)


shinyServer(function(input, output) {
  
  # PART 1A: JOB DUTIES / WORD TREE
  output$wordtree = gwordtree::renderGwordtree({
    col = paste(gsub(' ','.',input$title),'.',gsub(' ','.',input$explevel),sep='')

    if (length(input$explevel)<2) {
      d = as.vector(data1[,col])
    }
    else {
      d = c()
      for (i in col) {
        d = c(d,as.vector(data1[,i]))
      }
    }
    d = d[d != ''] # filter out null values
    gwordtree::gwordtree(word = d, firstword = "To")
  })
  output$tit1 = renderText({paste(input$title,'is expected')})
  
  # PART 1B: HARD & DOMAIN SKILLS / WORD CLOUD
  output$wordcloud = renderPlot({
    # Set color
    colorPalette='Dark2'
    if(!colorPalette %in% rownames(brewer.pal.info)) colors = colorPalette else colors = brewer.pal(8, colorPalette)

    col = paste(gsub(' ','.',input$title),'.',gsub(' ','.',input$explevel),sep='')
    kw = as.vector(data2$keyword)
    if (length(input$explevel)<2) {
      freq = as.vector(data2[,col])
      wordcloud(kw,freq, max.words = input$maxword, scale = c(6,.8), random.order=FALSE, rot.per=0.5, use.r.layout=T, colors=colors, family = 'serif')
      title(main=input$explevel,cex.main=2,family='serif')
    }
    else {
      freq = data2[,col]
      inputlength = length(input$explevel)
      par(mfrow=c(1,inputlength))
      for (i in c(1:inputlength)) {
        wordcloud(kw,as.vector(freq[,i]), max.words = input$maxword, scale = c(6,.8), random.order=FALSE, rot.per=0.5, use.r.layout=T, colors=colors, family = 'serif')
        title(main=input$explevel[i],cex.main=2,family='serif')}
    }
  })
  output$tit2 = renderText({paste(input$title,'is required to have')})


  # PART 2A: MIN YEAR OF EXP / STACKED BAR
  output$stackedbar2 = renderPlot({
    df = data4[(data4$title_v3==input$title) & (data4$exp_level_v3 %in% input$explevel),]
    
    # Replace NAs exp_year with Not required and othesr with Required
    df[!is.na(df$exp_year),'exp_year_req'] = 'Required'
    df[is.na(df$exp_year),'exp_year_req'] = 'Not required'
    df$exp_year_req = factor(df$exp_year_req)

    # Annotation
    values = data.frame(table(df$exp_year_req, df$exp_level_v3))
    colnames(values) = c('Required','Level','Freq')
    values$Prop = round(values$Freq/nrow(df),3)
    
    #get rid of zero frequencies
    values = values[values$Freq>0,]

    fig = ggplot(data=values,aes(x=input$title, y = Prop, fill=Required)) + geom_col() + coord_flip() +
      xlab(NULL) +  scale_y_continuous('Proportion of Jobs', breaks = NULL) +
      scale_fill_brewer(palette = 'GnBu') +
      geom_text(aes(label = paste(Prop*100,'%'), fontface='bold', size = 18, family = 'serif'),
                position = position_stack(vjust = 0.5), show.legend = FALSE) +
      facet_grid(rows = vars(Level)) +
      theme(panel.background = element_blank(),
            legend.position="top",
            legend.text = element_text(colour = "black", size = 22, face = 'bold', family = 'serif'),
            legend.title = element_blank(),
            legend.box.spacing = unit(0,'cm'),
            legend.spacing.x = unit(0.5, 'cm'),
            axis.ticks  = element_blank(),
            axis.title.x = element_text(size = 18, family = 'Palatino'),
            axis.text.y = element_text(size = 18, family = 'Palatino')
      )

    fig

  })

  # PART 2B: MIN YEAR OF EXP + MIN EDUCATION LEVEL / COMBINED BAR & LINE CHART
  output$combchart = renderPlotly({
    df = data4[(data4$title_v3==input$title) & (data4$exp_level_v3 %in% input$explevel),]
    
    # Annotation values

    values = df[!is.na(df$exp_year),]
    if (input$average == 'Mean') {
      values = aggregate(values$exp_year,by=list(values$min_degree,values$exp_level_v3),mean)
      values$x = round(values$x,1)
      metric = 'mean'} else {
      values = aggregate(values$exp_year,by=list(values$min_degree,values$exp_level_v3),median)
      metric = 'median'}

    fig = ggplot(data=df,aes(x=min_degree)) +
      geom_bar(aes(fill="Number of Jobs")) + ylab('Number of Jobs') + xlab(NULL) +
      stat_summary(aes(y=exp_year*(nrow(df)/20)), fun.y = metric, na.rm = T, size = 3, color = 'grey30', geom = "point") +
      stat_summary(aes(y=exp_year*(nrow(df)/20), group = 1, linetype='Min Years of Exp'), fun.y = metric, na.rm = T, color = 'grey30', geom = "line") +
      stat_summary(aes(y=exp_year*(nrow(df)/25)), fun.y = metric, na.rm = T, color = 'black', geom = "text", vjust = 20, hjust = 5, size = 3, label = values$x) +
      scale_linetype_manual(name=NULL,values = c('Min Years of Exp'='dashed')) +
      scale_fill_manual(name=NULL,values = c("Number of Jobs"='steelblue')) +
      facet_grid(cols = vars(exp_level_v3)) +
      theme(panel.border = element_blank(),
            panel.grid = element_blank(),
            panel.background = element_rect(fill='whitesmoke'),
            legend.margin = margin(t = 5, r = 5, b = 5, l = 5, unit = "pt"),
            legend.text = element_text(colour = "black", size = 13, face = 'bold', family = 'serif'),
            axis.title.y = element_text(size = 13, family = 'Palatino'),
            axis.text.x = element_text(size = 13, family = 'Palatino')
      )
    fig = ggplotly(fig, tooltip = c("count")) %>% layout(legend = list(orientation = "h", x = 0.4, y = -0.2))
    fig
  })

  # PART 3A: DEMAND BY COUNTRY / TREE MAP
  output$treemap = renderGvis({
    
    get.continent = function(country) {
      if (country %in% c('Australia','China','India','Japan','Singapore')) {
        return ('Asia Pacific')}
      else if (country %in% c('United States','Canada')) {return ('North America')}
      else if (country == 'South Africa') {return ('Africa')}
      else {return ('Europe')}
    }
    
    df = data4[(data4$title_v3==input$title) & (data4$exp_level_v3 %in% input$explevel),c('country','area')]
    
    df$freq = 1
    
    # Update area with name same as country to Others
    levels(df$area)[levels(df$area) %in% levels(df$country)] = paste('Others in',levels(df$area)[levels(df$area) %in% levels(df$country)])
    
    # Aggregate data
    area_level = aggregate(list(area.jobs=df$freq),list(country=df$country,area=df$area),sum)
    area_level$continent = as.vector(sapply(area_level$country,get.continent))
    continent_level = aggregate(list(continent.jobs=area_level$area.jobs),list(continent=area_level$continent),sum)
    country_level = aggregate(list(country.jobs=area_level$area.jobs),list(continent=area_level$continent,country=area_level$country),sum)
    n = nrow(continent_level)
    
    # Final data
    my.data = data.frame(regionid = c("World",
                                      as.character(continent_level$continent),
                                      as.character(country_level$country),
                                      as.character(area_level$area)),
                         parentid = c(NA,rep("World",n),
                                      as.character(country_level$continent),
                                      as.character(area_level$country)),
                         jobs = c(sum(area_level$area.jobs),
                                  continent_level$continent.jobs,
                                  country_level$country.jobs,
                                  area_level$area.jobs)
    )
    my.data$color.range=log(my.data$jobs)
    
    gvisTreeMap(my.data, "regionid", "parentid",
                "jobs", "color.range",
                options=list(width="100%", height="500px",
                             fontSize=14,
                             minColor='#deebf7',
                             midColor='#9ecae1',
                             maxColor='#3182bd',
                             headerHeight=50,
                             fontColor='black',
                             showScale=TRUE,
                             showTooltips=TRUE))
    
  })

  # PART 3B: DEMAND BY INDUSTRY / BAR
  output$bar = renderPlotly({
    col = paste(gsub(' ','.',input$title),'.',gsub(' ','.',input$explevel),sep='')

    df = data3[,c('industry_v2',col)]

    njob = nrow(data4[(data4$title_v3==input$title) & (data4$exp_level_v3 %in% input$explevel),])

    # sum values over all exp levels
    if (length(input$explevel) > 1) {
      df = cbind(df,rowSums(df[,c(2:(length(input$explevel)+1))]))
      df = df[c(1,length(input$explevel)+2)]
      }

    colnames(df) = c('Industry','Freq')
    df['Proportion'] = round((df$Freq)*100/njob,3)
    newlevels = levels(df$Industry)[order(df$Freq,decreasing = FALSE)]
    df$Industry = factor(df$Industry,levels = newlevels)
    df = df[order(df$Freq,decreasing=T),]
    df = df[1:input$maxind,]

    bar = ggplot(data=df, aes(x=Industry, y=Proportion)) + geom_col(fill='steelblue4') + coord_flip() +
      ylab('Proportion of Jobs') +
      theme(panel.background = element_blank(),
            axis.title = element_text(size = 13, family = 'Palatino'),
            axis.text = element_text(size = 13, family = 'Palatino')
            )
    bar = ggplotly(bar, tooltips = c("x","label"), width = 1200, height = 800)
    bar = bar %>% layout(yaxis = NULL)
  })
  

  # PART 4: JOB LISTINGS
  output$listing = renderUI({ 
    
    df = data4[(data4$country==input$country) & (data4$title_v3==input$title) & (data4$exp_level_v3 %in% input$explevel),]

    if (nrow(df) == 0) {
      helpText("No jobs found. Reset your criteria")}
    else {
    lapply(1:nrow(df), function(i) {
      wellPanel(
      tagList(
        tags$a(href = df[i,'link'],tags$h3(strong(df[i,'title_v2']),style='font-size:20px')),
        tags$h4(df[i,'company']),
        tags$h5(paste(df[i,'area'],df[i,'country'],sep=', '),style='color:grey'),
        tags$p(paste0(substr(df[i,'text'],1,200)),'...'),
        tags$h5(toupper(paste(df[i,'job_type_v2'],df[i,'exp_level_v3'],sep=' | ')),style='color:grey')
      ), style = 'width:80%'
      )
      })
    }
  })
  
  # PART 5: FUN FACTS
  output$d3 <- renderD3({
    data = data.frame(x = c(100,400,700,1000),
                      t1 = c('10,368','123','16','6'),
                      t2 = c('jobs','industries','countries','positions'),
                      t3 = c('The raw dataset contains 11,697 job postings from over 5000 companies in the world.',
                             'Technology and internet-service companies are in greatest need for Data Science positions.',
                             'I collected job data from 5 continents, 16 countries and 256 states/areas.',
                             'Besides Data Scientist (which accounts for 48.6% in my data), I am also able to collect sufficient data for 5 other Data Science positions usually mistaken with Data Scientist,' 
                      ),
                      t4 = c('After removing duplications and other data cleansing steps, 10,368 different job postings remain ready for analysis.', 
                             'However, as technological advances have transformed all kinds of businesses, opportunities are prevalent in non-tech sectors as well.',
                             'Data Science is an emerging field, so I only focused on developed nations with fast-growing tech landscape.',
                             'including Data Analyst, Data Engineer, Machine Learning Engineer, Big Data Developer and Analytics Consultant. The differences among these positions are of special interest to me.'
                      )
    )
    r2d3(data = data, script = "circle.js")
  })
  
  # PART 6: QUICK INSIGHTS
  output$insight = renderUI({
    df = data5[data5$title == input$title,]
    tags$ul(
      tags$li('There are',strong(df$jobs),'hiring positions for',input$title, style = 'margin-bottom:3px;'),
      tags$li(strong(df$skill),'are the most required skills by employers.', style = 'margin-bottom:3px;'),
      tags$li('Only',strong(df$need_degree),'of hiring positions for',strong(input$title), 'require a degree. A candidate is expected to have at least a',strong(df$degree),'.', style = 'margin-bottom:3px;'),
      tags$li(strong(df$need_experience),'of employers specify the number of years of experience required. A qualified applicant should have at the minimum of',strong(df$experience),'years of experience.', style = 'margin-bottom:3px;'),
      tags$li(strong(df$country),'are where',strong(input$title), 'is highest sought after.', style = 'margin-bottom:3px;'),
      tags$li('Besides IT-related sectors,',strong(df$industry),'are the most promising industries to find a job.'),
      style='list-style-type:circle;'
    )
  })
  
  
})
