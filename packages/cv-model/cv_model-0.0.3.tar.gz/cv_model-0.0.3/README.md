# cv-model

- Roadmap
  - markdown encoder & decoder
  - watchdog


I want to start working on a full stack project. The idea is to help ordinary people write resume in a professional way.

- frontend: nextjs
  - Side by side view
    - left side: editor
      - represent resume as either json or yaml, or anything that can be validated by a schema
      - alternatively, a UI form that will ask user input for each field in the schema
    - right side: preview
      - show the resume in a professional way, with a few templates to choose from
      - allow user to download the resume as pdf, docx, etc.
- backend: python (fastapi, typst, jinja2)
    - front end will pass validated json resume data to backend
    - backend pipeline:
      - validate the json resume data against pydantic model
      - generate typst script from json data and jinja template
      - generate pdf from typst script
      - return the pdf to front end for preview/download
- deployment: I am not sure yet, I need some help here
  - I am thinking of using vercel for frontend
  - Some cloud service for backend, like AWS, GCP, or Azure

Future roadmap:
- generate a website from the json resume data automatically for the user
- use llm to help user write resume
- use llm to fine-tune the resume based on job description

Comparison with rendercv:
- rendercv use its own schema which is not compatible with jsonresume schema
- rendercv only support yaml format, while I want to support json and yaml and ui form

- [resume-schema](https://github.com/jsonresume/resume-schema)
- [rendercv](https://github.com/rendercv/rendercv/tree/main)
