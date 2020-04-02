def rich(bilal):

    try:
        file1 = open('templates/'+str(bilal['job-code'])+'.html',"w", encoding='utf-8')
    except:
        file1 = open('templates/'+str(bilal['jobid'])+'.html',"w", encoding='utf-8')

    file1.write("<html>"+'\n'+"<head>"+"\n"+"<title>")
    
    file1.write(bilal['title'])

    file1.write("</title>"+'\n'+'<script type="application/ld+json">'+'\n'+'{'+'\n'+'"@context" : "https://schema.org/",'+'\n')
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
    file1.write('",'+'\n'+'"unitText": ""'+'\n'+'}'+'\n'+'}'+'\n'+'}')

    file1.write("</script>"+'\n'+"</head>"+'\n'+"<body>"+'\n'+"</body>"+"\n"+"</html>")

    file1.close()
