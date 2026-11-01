# About 

- This is a simple in memory rag system all the files are in `src/rag/` 
- This project has the following: 
    1- Direct connection to ollama 
    2- Embeding model (ollama)
    3- An llm (ollama) 
    4- Chunking
    5- Vectorizing the chunks 
    6- Retrieval 
    7- Chat interface
- All the docs are in `src/rag/docs/` so the main script `main.py` can immediately read them if you want to have them at the root directory you could just simple move the folder back and add .parent (depending on how many folders you went back you would need to add more .parent for example (.parent.parent you went back once imagine it as `cd ..`))  in this for loop `for file in Path("docs").glob("*.md"):` just add it to the end before the : you would you be able to make the codebase structure a bit cleaner personally I like it like this enhence why I didn't change

Overall in memory chat interface to help understand rag in a smaller scale project