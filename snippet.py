def rich(bilal):

    try:
        file1 = open('templates/'+str(bilal['job-code'])+'.html',"w", encoding='utf-8')
    except:
        file1 = open('templates/'+str(bilal['jobid'])+'.html',"w", encoding='utf-8')

    file1.write("<!DOCTYPE html>"+'\n')
    file1.write("<html>"+'\n'+"<head>"+"\n"+"<title>")
    
    file1.write(bilal['title'])

    file1.write("</title>"+'\n'+'<link href="./assets/css/material-kit.css?v=2.0.7" rel="stylesheet" />'+'\n'+'<script type="application/ld+json">'+'\n'+'{'+'\n'+'"@context" : "https://schema.org/",'+'\n')
    file1.write('"@type" : "JobPosting",'+"\n")
    file1.write('"title" : "')
    file1.write(bilal['title'])

    file1.write('",'+'\n'+'"description" : ')

    file1.write('"')
    file1.write(bilal['description'])
    file1.write('",')

    file1.write('\n'+'"datePosted" : "')
    try:
        file1.write(bilal['posted-date'].split('T')[0])
    except:
        file1.write(bilal['date'].split('T')[0])

    file1.write('",'+'\n'+'"validThrough" : "')
    try:
        file1.write(bilal['posted-date'])
    except:
        file1.write(bilal['date'])

    file1.write('",'+'\n'+'"employmentType" : "')
    file1.write(bilal['jobtype'])

    file1.write('",'+'\n'+'"hiringOrganization" : {'+'\n'+'"@type" : "Organization",'+'\n'+'"name" : "')
    file1.write(bilal['company'])

    file1.write('",'+'\n'+'"sameAs" : "')
    file1.write(bilal['url'])

    file1.write('",'+'\n'+'"logo" : "')
    file1.write(bilal['logo'])

    file1.write('"'+'\n'+'},'+'\n'+'"jobLocation": {'+'\n'+'"@type": "Place",'+'\n'+'"address": {'+'\n'+'"@type": "PostalAddress",'+'\n'+'"streetAddress": "",'+'\n'+'"addressLocality": "",'+'\n'+'"addressRegion": "')
    file1.write(bilal['state'])

    file1.write('",'+'\n'+'"postalCode" : "')
    file1.write('",'+'\n'+'"addressCountry" : "')
    file1.write(bilal['country'])

    file1.write('"'+'\n'+'}'+'\n'+'},'+'\n'+'"baseSalary": {'+'\n'+'"@type": "MonetaryAmount",'+'\n'+'"currency": "')
    file1.write(bilal['currency'])

    file1.write('",'+'\n'+'"value": {'+'\n'+'"@type": "QuantitativeValue",'+'\n'+'"value": "')
    file1.write('",'+'\n'+'"unitText": ""'+'\n'+'}'+'\n'+'}'+'\n'+'}'+'\n')

    file1.write("</script>"+'\n'+"</head>"+'\n')
    file1.write('<body class="profile-page sidebar-collapse"><nav class="navbar navbar-transparent navbar-color-on-scroll fixed-top navbar-expand-lg" color-on-scroll="100" id="sectionsNav"><div class="container"><div class="navbar-translate"><a class="navbar-brand" href="https://demos.creative-tim.com/material-kit/index.html">Refringo </a></div></div></nav><div class="page-header header-filter" data-parallax="true" style="background-image: url(')
    file1.write("'./assets/img/city-profile.jpg'")
    file1.write(');"></div><div class="main main-raised"><div class="profile-content"><div class="container"><div class="row"><div class="col-md-8 ml-auto mr-auto"><div class="profile"><div class="avatar"><img src="')
    file1.write(bilal['logo'])
    file1.write('" alt="Circle Image" class="img-raised rounded-circle img-fluid"></div><div class="name"><h3 class="title" id="company">')
    file1.write(bilal['company'])
    file1.write('</h3><h5 class="card-title" id="address">')
    file1.write(bilal['city']+', ')
    file1.write(bilal['country']+', ')
    file1.write(bilal['state'])
    file1.write('</h5><h3 class="card-title" id="title">')
    file1.write(bilal['title'])
    file1.write('</h3><h5 class="card-subtitle mt-2"  id="job-type">')
    file1.write(bilal['jobtype'])
    file1.write('</h5>')
    file1.write('</h3>'+'\n')
    file1.write('<div class="card-text mt-2" style="justify-content: flex-start;text-align: left;" id="description">')
    file1.write(bilal['description'])
    file1.write('</div>')
    file1.write('<a href="')
    file1.write(bilal['url'])
    file1.write('" class="btn btn-primary">Apply Now</a></div></div></div></div></div></div></div>')

    file1.write("\n"+"</body>""\n"+"</html>")

    file1.close()
