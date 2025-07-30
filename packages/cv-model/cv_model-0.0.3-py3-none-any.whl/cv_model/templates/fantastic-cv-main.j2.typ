

#let render_font = "{{ ctx.font_family }}"
#let render_size = {{ ctx.font_size }}pt
#let render_size_title = render_size * 1.5
#let render_size_section = render_size * 1.3
#let render_size_entry = render_size * 1.1
#let render_page_paper = "{{ ctx.page_size }}"

#let render_space_between_sections = {{ ctx.section_spacing }}em
#let render_space_between_entry = {{ ctx.entry_spacing }}em
#let render_space_between_highlight = {{ ctx.highlight_spacing }}em

#let section_order = (
  {% for section_name in ctx.section_order %}
  "{{ section_name|lower|replace(" ", "_") }}",
  {% endfor %}
)

#set text(
  font: "{{ ctx.font_family }}",
  size: render_size,
  lang: "en",
  ligatures: false,
  fill: rgb("{{ ctx.text_color }}"),
)

#set page(
  margin: (
    top: {{ ctx.page_margin.top }}in,
    bottom: {{ ctx.page_margin.bottom }}in,
    left: {{ ctx.page_margin.left }}in,
    right: {{ ctx.page_margin.right }}in,
  ),
  paper: "{{ ctx.page_size }}",
)

#set par(justify: true)

#show link: underline

#show link: set text(fill: rgb("{{ ctx.link_color }}"))

// name heading
#show heading.where(level: 1): it => [#text(
  render_size_title,
  weight: "extrabold",
  rgb("{{ ctx.name_color }}")
)[#it]]

// section heading
#show heading.where(level: 2): it => [#text(
  render_size_section,
  weight: "bold",
  rgb("{{ ctx.section_title_color }}")
)[#it]]

// entry heading
#show heading.where(level: 3): it => [#text(
  render_size_entry,
  weight: "semibold",
  rgb("{{ ctx.entry_title_color }}")
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
        if highlight.summary.len() == 0 {
          description_str = ""
        }
        [- #text(weight: "bold")[#summary_str]#description_str]
      })
      .join(v(render_space_between_highlight))
  }
  _section(_custom_section.title, section_body)
}



#let name = "{{ resume.basics.name }}"
#let location = "{{ resume.basics.location.city }}, {{ resume.basics.location.region }}"
#let email = "{{ resume.basics.email }}"
#let phone = "{{ resume.basics.phone }}"
#let url = "{{ resume.basics.url }}"

// [{network: str, username: str, url: str}]
#let profiles = (
{% for profile in resume.basics.profiles %}
  (
    network: "{{ profile.network }}",
    username: "{{ profile.username }}",
    url: "{{ profile.url }}",
  ),
{% endfor %}
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
{% for education in resume.education %}
  (
    institution: "{{ education.institution }}",
    location: "{{ education.location }}",
    url: "{{ education.url }}",
    area: "{{ education.area }}",
    studyType: "{{ education.studyType }}",
    startDate: "{{ education.startDate }}",
    endDate: "{{ education.endDate }}",
    score: "{{ education.score }}",
    courses: (
{% for course in education.courses %}
      "{{ course }}",
{% endfor %}
    ),
  ),
{% endfor %}
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
{% for work in resume.work %}
  (
    name: "{{ work.name }}",
    location: "{{ work.location }}",
    url: "{{ work.url }}",
    description: "{{ work.description }}",
    position: "{{ work.position }}",
    startDate: "{{ work.startDate }}",
    endDate: "{{ work.endDate }}",
    highlights: (
{% for hl in work.highlights_typst %}
      [{{ hl }}],
{% endfor %}
    ),
  ),
{% endfor %}
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
{% for project in resume.projects %}
  (
    name: "{{ project.name }}",
    url: "{{ project.url }}",
    source_code: "{{ project.source_code }}",
    roles: ({% for role in project.roles %}"{{ role }}"{% if not loop.last %}, {% endif %}{% endfor %}),
    startDate: "{{ project.startDate }}",
    endDate: "{{ project.endDate }}",
    description: "{{ project.description }}",
    highlights: (
{% for hl in project.highlights_typst %}
      [{{ hl }}],
{% endfor %}
    ),
  ),
{% endfor %}
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
{% for volunteer in resume.volunteer %}
  (
    organization: "{{ volunteer.organization }}",
    position: "{{ volunteer.position }}",
    url: "{{ volunteer.url }}",
    startDate: "{{ volunteer.startDate }}",
    endDate: "{{ volunteer.endDate }}",
    summary: "{{ volunteer.summary }}",
    location: "{{ volunteer.location }}",
    highlights: (
{% for hl in volunteer.highlights_typst %}
      [{{ hl }}],
{% endfor %}
    ),
  ),
{% endfor %}
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
{% for award in resume.awards %}
  (
    title: "{{ award.title }}",
    date: "{{ award.date }}",
    url: "{{ award.url }}",
    awarder: "{{ award.awarder }}",
    summary: "{{ award.summary }}",
  ),
{% endfor %}
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
{% for certificate in resume.certificates %}
  (
    name: "{{ certificate.name }}",
    issuer: "{{ certificate.issuer }}",
    url: "{{ certificate.url }}",
    date: "{{ certificate.date }}",
  ),
{% endfor %}
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
{% for publication in resume.publications %}
  (
    name: "{{ publication.name }}",
    publisher: "{{ publication.publisher }}",
    releaseDate: "{{ publication.releaseDate }}",
    url: "{{ publication.url }}",
    summary: "{{ publication.summary }}",
  ),
{% endfor %}
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
{% for custom_section in resume.custom_sections %}
{% set section_id = custom_section.title|lower|replace(" ", "_") %}
#let custom_section_{{ section_id }} = (
  title: "{{ custom_section.title }}",
  highlights: (
{% for highlight in custom_section.highlights_typst %}
    (
      summary: "{{ highlight.summary }}",
      description: [{{ highlight.description }}],
    ),
{% endfor %}
  )
)
{% endfor %}

#render_basic_info(
  name: name,
  location: location,
  email: email,
  phone: phone,
  url: url,
  profiles: profiles,
)

{% for section_title in ctx.section_order %}
{% if section_title == "education" %}
#render_education(educations)
{% elif section_title == "work" %}
#render_work(works)
{% elif section_title == "projects" %}
#render_project(projects)
{% elif section_title == "volunteer" %}
#render_volunteer(volunteers)
{% elif section_title == "awards" %}
#render_award(awards)
{% elif section_title == "certificates" %}
#render_certificate(certificates)
{% elif section_title == "publications" %}
#render_publication(publications)
{% else %}
#render_custom(custom_section_{{ section_title|lower|replace(" ", "_") }})
{% endif %}
{% endfor %}
