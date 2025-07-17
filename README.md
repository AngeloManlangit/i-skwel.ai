# I-skwel.ai

<img width="1134" height="909" alt="image" src="https://github.com/user-attachments/assets/b69336d7-32d8-4d34-a7a9-e50b5e5f5810" />

## About the Project

I-skwel.ai is your AI-Powered Learning Roadmap Platform to Success, designed to help STEM Students make logical choices regarding their futures. **Discover** what's in store for you in any college course with this application, empowering you to navigate your academic path with confidence and prior knowledge.

This project is for Team M & 'Ems submission for the [**𝗖𝗮𝗻 𝗬𝗼𝘂 𝗛𝗮𝗰𝗸𝗜𝗧: 𝗧𝗵𝗲 𝗜𝗕𝗣𝗔𝗣 𝗖𝗵𝗮𝗹𝗹𝗲𝗻𝗴𝗲 (𝗖𝗬𝗛)**](https://www.facebook.com/share/p/1FrqsGx4sg/).

## How to Use

Using **I-skwel.ai** is simple!
1. Let the AI get to know you!
   - Input a brief overview of who you are
   - Provide your interests, skills, and even your weaknesses so that we can get an idea on who you are and what you might like in a program
   - The data you input affects the suggestions for courses and schools that will be shown in the roadmap
2. Input your location (optional)
   - You don't have to put your location if you don't want to but it would help in gathering data and finding school nearest to you
3. Click on "Generate Roadmap 🚀"
  - Begin generating your roadmap with all the data you inputted!

## Technologies Used

### Front-End
- Vite
- Vue.js
- Tailwind CSS

### Back-End
  - Python
  - Javascipt
  - SQLite3
  - Node.js - to run the vite build
  - python-flask
  - Vue Flow - for the flowchart
  - ChromaDB - for initializing vector database
 
### AI Used
  - MiniLM-L6-v2 - used by chromaDB as a Sentence Transformer 
  - Gemini 2.5 Flash
 
## Using the Program

### Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

### Project Setup

#### Clone the github repository
```sh
git clone https://github.com/[username]/i-skwel.ai.git
```

#### Download the dependencies

```sh
npm install
```

To include Vue Flow and Tailwind into your application, run:
```sh
npm install @vue-flow/core tailwindcss @tailwindcss/vite
```

Follow the installation processes of [Vue Flow](https://vueflow.dev/guide/getting-started.html) and [Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite) with Vite on their websites.

#### Setup your .env file
./I-skwel.ai/.env:
```
VITE_GEMINI_API_KEY=(your Gemini 2.5 API Key)
```
*Place your .env file in the same folder as App.vue*

#### Install the following Python libraries
```
pip install pandas chromadb google-genai python-dotenv Flask Flask-Cors
```
### Initialize vector database (skip if it has been initialized already)
```
python fill_db_new.py
```

#### Run pyhthon flask-backend server
```
python run backend_api.py
```

#### Compile and Hot-Reload for Development

```sh
npm run dev
```

or Compile and Minify for Production using:

```sh
npm run build
```
