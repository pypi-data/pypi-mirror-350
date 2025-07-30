

#let render_font = "New Computer Modern"
#let render_size = 12pt
#let render_size_title = render_size * 1.5
#let render_size_section = render_size * 1.3
#let render_size_entry = render_size * 1.1
#let render_page_paper = "a4"

#let render_space_between_sections = -0.5em
#let render_space_between_entry = -0.5em
#let render_space_between_highlight = 0em


#set text(
  font: "New Computer Modern",
  size: render_size,
  lang: "en",
  ligatures: false,
  fill: rgb("#000000"),
)

#set page(
  margin: (
    top: 0.5in,
    bottom: 0.5in,
    left: 0.5in,
    right: 0.5in,
  ),
  paper: "a4",
)

#set par(justify: true)

#set list(tight: true)

#show link: underline

#show link: set text(fill: rgb("#26428b"))

// name heading
#show heading.where(level: 1): it => [#text(
  render_size_title,
  weight: "extrabold",
  rgb("#000000")
)[#it]]

// section heading
#show heading.where(level: 2): it => [#text(
  render_size_section,
  weight: "bold",
  rgb("#26428b")
)[#it]]

// entry heading
#show heading.where(level: 3): it => [#text(
  render_size_entry,
  weight: "semibold",
  rgb("#26428b")
)[#it]]

#let _format_dates(
  start-date: "",
  end-date: "",
) = {
  start-date + " " + $dash.em$ + " " + end-date
}


#let _entry_heading(
  main: "", // top left
  dates: "", // top right
  description: "", // bottom left
  bottom_right: "", // bottom right
) = {
  [
    === #main #h(1fr) #dates \
    #description #h(1fr) #bottom_right
  ]
}

#let _section(title, body) = {
 [ == #smallcaps(title)]
 v(-0.5em)
 line(length: 100%, stroke: stroke(thickness: 0.4pt))
  v(-0.5em)
  body
  v(render_space_between_sections)
}


#let render_basic_info(
  name: "",
  location: "",
  phone: "",
  email: "",
  url: "",
  profiles: [],
) = {
  set document(
    author: name,
    title: name,
    description: "Resume of " + name,
    keywords: "resume, cv, curriculum vitae",
  )

  align(
    left,
    [= #name #h(1fr) #location],
  )


  pad(
    top: 0.25em,
    [
      #{
        let items = (
          phone,
          link(email)[#email],
          link(url)[#url],
        )
        items.filter(x => x != none).join("  |  ")
        "  |  "
        profiles
          .map(profile => {
            profile.network + ": "
            link(profile.url)[#profile.username]
          })
          .join("  |  ")
      }
    ],
  )
}

#let render_education(_educations) = {
  if _educations.len() == 0 {
    return
  }
  let section_body = {
    _educations
      .map(education => {
        let main = link(education.url)[#education.institution]
        if education.url.len() == 0 {
          main = education.institution
        }
        _entry_heading(
          main: main,
          dates: _format_dates(start-date: education.startDate, end-date: education.endDate),
          description: (
            emph(education.studyType),
            education.area,
            "GPA: " + strong(education.score),
          ).join(" | "),
          bottom_right: education.location,
        )
        [
          - #emph[Selected coursework]: #education.courses.join(", ")
        ]
      })
      .join(v(render_space_between_entry))
  }
  _section("Education", section_body)
}

#let render_work(_works) = {
  if _works.len() == 0 {
    return
  }
  let section_body = {
    _works
      .map(work => {
        let main = link(work.url)[#work.name]
        if work.url.len() == 0 {
          main = work.name
        }
        [
          #_entry_heading(
            main: main,
            dates: _format_dates(start-date: work.startDate, end-date: work.endDate),
            description: (
              emph(work.position),
              work.description,
            ).join(" | "),
            bottom_right: work.location,
          )
          #work.highlights.map(it => [- #it]).join(v(render_space_between_highlight))
        ]
      })
      .join(v(render_space_between_entry))
  }
  _section("Work", section_body)
}

#let render_project(_projects) = {
  if _projects.len() == 0 {
    return
  }
  let section_body = {
    _projects
      .map(project => {
        let main = link(project.url)[#project.name]
        if project.url.len() == 0 {
          main = project.name
        }
        let source_code = link(project.source_code)[Source code]
        if project.source_code.len() == 0 {
          source_code = ""
        }
        [
          #_entry_heading(
            main: main,
            dates: _format_dates(start-date: project.startDate, end-date: project.endDate),
            description: project.roles.map(emph).join(" | "),
            bottom_right: source_code,
          )
          #v(-2em) \
          #project.description
          #project.highlights.map(it => [- #it]).join(v(render_space_between_highlight))
        ]
      })
      .join(v(render_space_between_entry))
  }
  _section("Projects", section_body)
}

#let render_volunteer(_volunteers) = {
  if _volunteers.len() == 0 {
    return
  }
  let section_body = {
    _volunteers
      .map(volunteer => {
        let main = link(volunteer.url)[#volunteer.organization]
        if volunteer.url.len() == 0 {
          main = volunteer.organization
        }
        [
          #_entry_heading(
            main: main,
            dates: _format_dates(start-date: volunteer.startDate, end-date: volunteer.endDate),
            description: emph(volunteer.position),
            bottom_right: volunteer.location,
          )
          #v(-2em) \
          #volunteer.summary
          #volunteer.highlights.map(it => [- #it]).join(v(render_space_between_highlight))
        ]
      })
      .join(v(render_space_between_entry))
  }
  _section("Volunteering", section_body)
}

#let render_award(_awards) = {
  if _awards.len() == 0 {
    return
  }
  let section_body = [
    #(
      _awards
        .map(award => {
          let awarder_str = " - Awarded by " + award.awarder
          if award.awarder.len() == 0 {
            awarder_str = ""
          }
          let prefix = link(award.url)[#award.title]
          if award.url.len() == 0 {
            prefix = award.title
          }
          let summary_str = [#award.summary]
          if award.summary.len() == 0 {
            summary_str = ""
          }
          [- #prefix#awarder_str #h(1fr) #award.date \ #summary_str]
        })
        .join(v(render_space_between_highlight))
    )
  ]
  _section("Awards", section_body)
}

#let render_certificate(_certificates) = {
  if _certificates.len() == 0 {
    return
  }
  let section_body = _certificates
    .map(certificate => {
      let post_fix = h(1fr) + certificate.date
      let issue_str = " - issued by " + certificate.issuer
      if certificate.issuer.len() == 0 {
        issue_str = ""
      }
      let prefix = link(certificate.url)[#certificate.name]
      if certificate.url.len() == 0 {
        prefix = certificate.name
      }
      [- #prefix#issue_str #post_fix]
    })
    .join(v(render_space_between_highlight))
  _section("Certificates", section_body)
}



#let render_publication(_publications) = {
  if _publications.len() == 0 {
    return
  }
  let section_body = [
    #(
      _publications
        .map(publication => {
          let prefix = link(publication.url)[#publication.name]
          if publication.url.len() == 0 {
            prefix = publication.name
          }
          let publisher_str = " - published by " + publication.publisher
          if publication.publisher.len() == 0 {
            publisher_str = ""
          }
          let summary_str = [#publication.summary]
          if publication.summary.len() == 0 {
            summary_str = ""
          }
          [- #prefix#publisher_str #h(1fr) #publication.releaseDate \ #summary_str]
        })
        .join(v(render_space_between_highlight))
    )
  ]
  _section("Publications", section_body)
}

#let render_custom(_custom_section) = {
  let section_body = {
    _custom_section.highlights
      .map(highlight => {
        let summary_str = highlight.summary + ": "
        let description_str = highlight.description
        if highlight.description.len() == 0 {
          description_str = ""
        }
        [- #text(weight: "bold")[#summary_str]#description_str]
      })
      .join(v(render_space_between_highlight))
  }
  _section(_custom_section.title, section_body)
}



#let name = "Austin Yu"
#let location = "Bay Area, CA"
#let email = "yuxm.austin1023@gmail.com"
#let phone = "+1 (xxx) xxx-xxxx"
#let url = "https://www.google.com"

// [{network: str, username: str, url: str}]
#let profiles = (
  (
    network: "GitHub",
    username: "austinyu",
    url: "https://github.com/austinyu",
  ),
  (
    network: "LinkedIn",
    username: "xinmiao-yu-619128174",
    url: "https://linkedin.com/in/xinmiao-yu-619128174",
  ),
)

/*
[
  {
    institution: str,
    location: str,
    url: str,
    area: str,
    studyType: str,
    startDate: str,
    endDate: str,
    score: str,
    courses: [str],
  }
]
*/
#let educations = (
  (
    institution: "Stanford University",
    location: "Stanford, CA",
    url: "https://stanford.edu",
    area: "Physics and Computer Science",
    studyType: "Bachelor of Science",
    startDate: "2019-09-01",
    endDate: "2023-06-01",
    score: "3.9/4.0",
    courses: (
      "Data Structures",
      "Algorithms",
      "Operating Systems",
      "Computer Networks",
      "Quantum Mechanics",
      "Linear Algebra",
      "Machine Learning",
      "Multivariable Calculus",
    ),
  ),
  (
    institution: "University of California, Berkeley",
    location: "Berkeley, CA",
    url: "https://berkeley.edu",
    area: "Computer Science",
    studyType: "Master of Science",
    startDate: "2023-08-01",
    endDate: "2025-05-01",
    score: "4.0/4.0",
    courses: (
      "Advanced Machine Learning",
      "Distributed Systems",
      "Cryptography",
      "Artificial Intelligence",
      "Database Systems",
      "Convex Optimization",
      "Natural Language Processing",
      "Computer Vision",
    ),
  ),
)


/*
[
  {
    name: str,
    location: str,
    url: str,
    description: str,
    position: str,
    startDate: str,
    endDate: str,
    highlights: [str],
  }
]
*/
#let works = (
  (
    name: "Microsoft",
    location: "Redmond, WA",
    url: "https://microsoft.com",
    description: "Azure Cloud Services Team",
    position: "Software Engineer Intern",
    startDate: "2023-05-15",
    endDate: "2023-08-15",
    highlights: (
      "Developed a distributed caching solution for Azure Functions, reducing cold start latency by 30% and improving overall performance for serverless applications.",
      "Implemented a monitoring dashboard using Power BI to visualize key performance metrics, enabling proactive issue detection and resolution.",
      "Collaborated with a team of engineers to refactor legacy code, improving maintainability and reducing technical debt by 25%.",
      "Contributed to the design and development of a new API gateway, enhancing scalability and security for cloud-based applications.",
      "Presented project outcomes to senior engineers and received commendation for delivering impactful solutions under tight deadlines.",
    ),
  ),
  (
    name: "Amazon",
    location: "Seattle, WA",
    url: "https://amazon.com",
    description: "Alexa Smart Home Team",
    position: "Software Development Engineer Intern",
    startDate: "2022-06-01",
    endDate: "2022-09-01",
    highlights: (
      "Designed and implemented a feature to integrate third-party smart home devices with Alexa, increasing compatibility by 20%.",
      "Optimized voice recognition algorithms, reducing error rates by 15% and improving user satisfaction.",
      "Developed automated testing frameworks to ensure the reliability of new integrations, achieving 90% test coverage.",
      "Worked closely with product managers to define feature requirements and deliver a seamless user experience.",
      "Participated in code reviews and contributed to team-wide best practices for software development.",
    ),
  ),
  (
    name: "Tesla",
    location: "Palo Alto, CA",
    url: "https://tesla.com",
    description: "Autopilot Software Team",
    position: "Software Engineer Intern",
    startDate: "2021-06-01",
    endDate: "2021-08-31",
    highlights: (
      "Developed and tested computer vision algorithms for lane detection, improving accuracy by 25% in challenging driving conditions.",
      "Enhanced the performance of real-time object detection systems, reducing processing latency by 10%.",
      "Collaborated with hardware engineers to optimize sensor data processing pipelines for autonomous vehicles.",
      "Conducted extensive simulations to validate new features, ensuring compliance with safety standards.",
      "Documented technical findings and contributed to research papers on advancements in autonomous driving technology.",
    ),
  ),
)

/*
[
  {
    name: str,
    url: str,
    source_code: str,
    roles: [str],
    startDate: str,
    endDate: str,
    description: str,
    highlights: [str],
  }
]
*/
#let projects = (
  (
    name: "Hyperschedule",
    url: "https://hyperschedule.io",
    source_code: "https://github.com/hyperschedule",
    roles: ("Individual Contributor", "Maintainer"),
    startDate: "2022-01-01",
    endDate: "Present",
    description: "Developed and maintained an open-source scheduling tool used by students across the Claremont Consortium, leveraging TypeScript, React, and MongoDB.",
    highlights: (
     "Implemented new features such as course filtering and schedule sharing, improving user experience and engagement.",
     "Collaborated with a team of contributors to address bugs and optimize performance, reducing load times by 40%.",
     "Coordinated with college administrators to ensure accurate and timely release of course data.",
    ),
  ),
  (
    name: "Claremont Colleges Course Registration",
    url: "",
    source_code: "https://github.com/claremont-colleges",
    roles: ("Individual Contributor", "Maintainer"),
    startDate: "2021-09-01",
    endDate: "2022-12-01",
    description: "Contributed to the development of a course registration platform for the Claremont Colleges, streamlining the enrollment process for thousands of students.",
    highlights: (
     "Designed and implemented a user-friendly interface for course selection, increasing adoption rates by 25%.",
     "Optimized backend systems to handle peak traffic during registration periods, ensuring system stability.",
     "Provided technical support and documentation to assist users and administrators with platform usage.",
    ),
  ),
)

/*
[
  {
    organization: str,
    position: str,
    url: str,
    startDate: str,
    endDate: str,
    summary: str,
    location: str,
    highlights: [str],
  }
]
*/
#let volunteers = (
  (
    organization: "Bay Area Homeless Shelter",
    position: "Volunteer Coordinator",
    url: "",
    startDate: "2023-01-01",
    endDate: "2023-05-01",
    summary: "Coordinated volunteer efforts to support homeless individuals in the Bay Area, providing essential services and resources.",
    location: "Bay Area, CA",
    highlights: (
      "Managed a team of 20+ volunteers to organize weekly meal services",
      "Collaborated with a team of volunteers to sort and package food donations, ensuring efficient distribution to partner agencies.",
      "Participated in community education initiatives, promoting awareness of food insecurity and available resources.",
    ),
  ),
  (
    organization: "Stanford University",
    position: "Volunteer Tutor",
    url: "stanford.edu",
    startDate: "2023-06-01",
    endDate: "2023-09-01",
    summary: "Provided tutoring support to high school students in mathematics and science subjects, fostering academic growth and confidence.",
    location: "Stanford, CA",
    highlights: (
      "Developed personalized lesson plans and study materials to address individual student needs.",
      "Facilitated group study sessions, encouraging collaboration and peer learning.",
      "Received positive feedback from students and parents for effective teaching methods and dedication to student success.",
    ),
  ),
)

/*
[
  {
    title: str,
    date: str,
    url: str,
    awarder: str,
    summary: str,
  }
]
*/
#let awards = (
  (
    title: "Best Student Award",
    date: "2023-05-01",
    url: "https://stanford.edu",
    awarder: "Stanford University",
    summary: "",
  ),
  (
    title: "Dean's List",
    date: "2023-05-01",
    url: "",
    awarder: "Stanford University",
    summary: "Achieved Dean's List status for maintaining a GPA of 3.9 or higher.",
  ),
  (
    title: "Outstanding Research Assistant",
    date: "2023-05-01",
    url: "https://stanford.edu",
    awarder: "",
    summary: "Recognized for exceptional contributions to research projects in the Physics and Computer Science departments.",
  ),
  (
    title: "Best Paper Award",
    date: "2023-05-01",
    url: "https://berkeley.edu",
    awarder: "University of California, Berkeley",
    summary: "Received Best Paper Award at the UC Berkeley Graduate Research Symposium.",
  ),
)

/*
[
  {
    name: str,
    issuer: str,
    url: str,
    date: str,
  }
]
*/
#let certificates = (
  (
    name: "AWS Certified Solutions Architect",
    issuer: "",
    url: "https://aws.amazon.com/certification/certified-solutions-architect-associate/",
    date: "2023-05-01",
  ),
  (
    name: "Google Cloud Professional Data Engineer",
    issuer: "Google Cloud",
    url: "https://cloud.google.com/certification/data-engineer/",
    date: "2023-05-01",
  ),
  (
    name: "Microsoft Certified: Azure Fundamentals",
    issuer: "Microsoft",
    url: "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/",
    date: "2023-05-01",
  ),
  (
    name: "Certified Kubernetes Administrator (CKA)",
    issuer: "Linux Foundation",
    url: "",
    date: "2023-05-01",
  ),
  (
    name: "Certified Ethical Hacker (CEH)",
    issuer: "",
    url: "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/",
    date: "2023-05-01",
  ),
)

/*
[
  {
    name: str,
    publisher: str,
    releaseDate: str,
    url: str,
    summary: str,
  }
]
*/
#let publications = (
  (
    name: "Understanding Quantum Computing",
    publisher: "Springer",
    releaseDate: "2023-05-01",
    url: "https://arxiv.org/abs/quantum-computing",
    summary: "A comprehensive overview of quantum computing principles and applications.",
  ),
  (
    name: "Machine Learning for Beginners",
    publisher: "O'Reilly Media",
    releaseDate: "2023-05-01",
    url: "",
    summary: "",
  ),
  (
    name: "Advanced Algorithms in Python",
    publisher: "Packt Publishing",
    releaseDate: "2023-05-01",
    url: "https://packt.com/advanced-algorithms-python",
    summary: "A deep dive into advanced algorithms and data structures using Python.",
  ),
  (
    name: "Data Science Handbook",
    publisher: "Springer",
    releaseDate: "2023-05-01",
    url: "",
    summary: "A practical guide to data science methodologies and tools.",
  ),
)


/*
custom sections
{
  title: str,
  highlights: [
    {
      summary: str,
      description: str,
    }
  ]
}
*/
#let custom_section_programming_languages = (
  title: "Programming Languages",
  highlights: (
    (
      summary: "Languages",
      description: "Python, Java, C++, JavaScript, TypeScript",
    ),
    (
      summary: "Frameworks",
      description: "React, Node.js, Express, Flask, Django",
    ),
    (
      summary: "Databases",
      description: "MySQL, MongoDB, PostgreSQL",
    ),
    (
      summary: "Tools",
      description: "Git, Docker, Kubernetes, AWS, GCP",
    ),
  )
)
#let custom_section_skills = (
  title: "Skills",
  highlights: (
    (
      summary: "Soft Skills",
      description: "Teamwork, Communication, Problem Solving, Time Management",
    ),
    (
      summary: "Technical Skills",
      description: "Data Structures, Algorithms, Software Development, Web Development",
    ),
    (
      summary: "Languages",
      description: "English (Fluent), Spanish (Conversational)",
    ),
  )
)

#render_basic_info(
  name: name,
  location: location,
  email: email,
  phone: phone,
  url: url,
  profiles: profiles,
)

#render_education(educations)

#render_work(works)

#render_project(projects)

#render_volunteer(volunteers)

#render_award(awards)

#render_certificate(certificates)

#render_publication(publications)

#render_custom(custom_section_programming_languages)

#render_custom(custom_section_skills)
