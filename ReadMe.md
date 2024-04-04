# Knowly
## _Advancing Conversational Data Interaction_

Knowly, is a knowledge-based self aware, Chat Application designed to revolutionize the way users interact with their data.
****

##### **To skip over features:**
- [Getting Started](#gettingstarted)
- [Demo](#demo)
- [Features](#features)
- [Tech](#tech)
- [FAQ](#faq)
- [LICENSE](#license)
****


## Getting Started
<a name="gettingstarted"></a>
Clone the **Knowly** github repository with 

```bash
  git clone https://github.com/mosszhd/knowly.git ./knowly_repo
```

Before cloning,
- Please ensure that you have [Python-3.10] or above installed.
- Please ensure that the [Ollama] app is installed in your device.

- **Once you have cloned the repository head over to the specified root directory:**
```bash
 cd ./knowly_repo
```
- **To install dependencies, run:**
```bash
  ./run.sh
``` 
- **To install the models without any efforts, run:**
```bash
    python get_models.py arg
```
The "arg" here is either '0' or '1'. '0' indicates a low PC configuration while '1' indicates a higher PC configuration. Default = 0
- **To Run The App:**
```bash
  streamlit run app.py
```
**NOTE:** 
- The source directory in this example is **"knowly_repo"**
- Please ensure that you have a virtual environment created before you run the scripts in the repository.           
****


## Demo
<a name="demo"></a>
To experience Knowly in action, witness our live demo [here].

**NOTE:**
- Be sure to start a new conversation everytime a data is uploaded into application. Not only does it allow the models to fully synchronize their knowledge with the data, but also helps them to capture better context from the data while during retrieval.

****


## Features
<a name="features"></a>
1. **Conversational Interface**: Picture prepping for exams and wishing you could just chat with your textbook to outline important questions. With Knowly, that's a reality - talk to your data and get the insights you need.

2. **Personalized Experience**: Unlike other AI chat apps, Knowly offers personalized results tailored to your needs. From organizing research papers to analyzing financial data, Knowly lets you curate your own knowledge base for relevant insights.

3. **Data Privacy in LLMs**: Concerned about data privacy? Knowly keeps your info safe by allowing you to track and manage shared documents, ensuring your privacy is always in your hands.

4. **Small Language Model Integration**: Knowly utilizes SOTA small language models for efficient and accurate data interactions, ensuring top-notch responsiveness.

5. **Multimodal Capabilities**: Knowly goes beyond text, processing images for deeper insights. Whether it's charts or graphs, Knowly empowers users to extract valuable information from various data sources.

6. **Audio Query**: Sick of typing? Knowly lets you talk to your data with audio input features, making data exploration hands-free and effortless!

7. **RAG Technology**: With RAG technology, Knowly breaks the boundaries of traditional chatbots, enabling seamless interaction with your text and image-based data.

8. **Model Switching**: Customize your experience with Knowly's model switching feature, optimizing for speed, accuracy, or linguistic diversity to suit your needs.

9. **Customizable Integration**: Seamlessly integrate Knowly with your existing data sources and workflows for a frictionless user experience, maximizing the potential of your data ecosystem.

In summary, Knowly revolutionizes data interaction, offering tailored insights and seamless integration to drive innovation and productivity in the digital age.
****


## Tech
<a name="tech"></a>
Knowly uses a number of open source projects to work properly:

- [chromadb] - Stores and manages vector embeddings.
- [ctransformers] - Powers conversational capabilities with transformers.
- [InstructorEmbedding] - Embeds instructions for retrieval QnA.
- [langchain] - Chain modules used for information retrieval from vector database. 
- [llama-cpp-python] - Enables seamless integration between C++ and Python (for Ollama). 
- [librosa] - Processes audio input for audio query feature.
- [pypdfium2] - Parses PDF document for data analysis. 
- [pyyaml] - Manages configuration files for customizable integration.
- [sentence-transformers] - Used for generating embeddings of parsed data.
- [streamlit] - Powers the WebUI of Knowly.
- [transformers] - Used for accessing Hugginface Transformer models.
- [unstructured] - Prepares raw documents for downstream ML tasks.
****



## FAQ
<a name="faq"></a>

### **Q: Is Knowly compatible with all types of data?**
**A:** Currently, Knowly supports "pdf" text files, as well as JPG, JPEG, and PNG image formats. While we encourage testing with other file types, progressive feedback is greatly appreciated.

### **Q: How does Knowly ensure data privacy?**
**A:** Knowly ensures data privacy by storing all user-interacted data locally on their machines. No data is shared online, ensuring privacy for both conversation history and interacted data. Users also have access to their uploaded data for transparency and awareness.

### **Q: Can Knowly be customized for specific use cases?**
**A:** Users can customize Knowly by uploading specific data for conversation. Each dataset creates a unique conversation, as the list of available models give data various personalities, enhancing inference. Further customization features are still under development. 

### **Q: How long does it take to setup the project?**
**A:** Setup time can range from seconds to almost an hour. Without Ollama locally, it may take over 45 minutes due to model optimizations. If models are present, setup is rather quick, often just a few minutes. 

## License
<a name="license"></a>
MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Python-3.10]: <https://www.python.org/downloads/>
   [Ollama]: <https://ollama.com/download>
   [here]: <http://>
