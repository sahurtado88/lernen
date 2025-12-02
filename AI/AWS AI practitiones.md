The bias versus variance trade-off refers to the challenge of balancing the error due to the model's complexity (variance) and the error due to incorrect assumptions in the model (bias), where high bias can cause underfitting and high variance can cause overfitting

The bias versus variance trade-off in machine learning is about finding a balance between bias (error due to overly simplistic assumptions in the model, leading to underfitting) and variance (error due to the model being too sensitive to small fluctuations in the training data, leading to overfitting). The goal is to achieve a model that generalizes well to new data.

Biases are imbalances in data or disparities in the performance of a model across different groups. Bias may also be introduced by the ML algorithm itself—even with a well-balanced training dataset, the outcomes might favor certain subsets of the data as compared to others.

This scenario illustrates algorithmic bias, where the hiring algorithm systematically favors candidates of a particular gender, indicating that there may be a bias in the training data or in the algorithm's design that leads to unequal treatment based on gender.

_________

Temperature– Affects the shape of the probability distribution for the predicted output and influences the likelihood of the model selecting lower-probability outputs.

Choose a lower value to influence the model to select higher-probability outputs.

Choose a higher value to influence the model to select lower-probability outputs.

In technical terms, the temperature modulates the probability mass function for the next token. A lower temperature steepens the function and leads to more deterministic responses, and a higher temperature flattens the function and leads to more random responses.

Top K – The number of most-likely candidates that the model considers for the next token.

Choose a lower value to decrease the size of the pool and limit the options to more likely outputs.

Choose a higher value to increase the size of the pool and allow the model to consider less likely outputs.

For example, if you choose a value of 50 for Top K, the model selects from 50 of the most probable tokens that could be next in the sequence.

Top P – The percentage of most-likely candidates that the model considers for the next token.

Choose a lower value to decrease the size of the pool and limit the options to more likely outputs.

Choose a higher value to increase the size of the pool and allow the model to consider less likely outputs.

In technical terms, the model computes the cumulative probability distribution for the set of responses and considers only the top P% of the distribution.

For example, if you choose a value of 0.8 for Top P, the model selects from the top 80% of the probability distribution of tokens that could be next in the sequence.

The following table summarizes the effects of these parameters.

Parameter	Effect of lower value	Effect of higher value
Temperature	Increase likelihood of higher-probability tokens
Decrease likelihood of lower-probability tokens

Increase likelihood of lower-probability tokens
Decrease likelihood of higher-probability tokens

Top K	Remove lower-probability tokens	Allow lower-probability tokens
Top P	Remove lower-probability tokens	Allow lower-probability tokens
As an example to understand these parameters, consider the example prompt I hear the hoof beats of ". Let's say that the model determines the following three words to be candidates for the next token. The model also assigns a probability for each word.


{
    "horses": 0.7,
    "zebras": 0.2,
    "unicorns": 0.1
}
If you set a high temperature, the probability distribution is flattened and the probabilities become less different, which would increase the probability of choosing "unicorns" and decrease the probability of choosing "horses".

If you set Top K as 2, the model only considers the top 2 most likely candidates: "horses" and "zebras."

If you set Top P as 0.7, the model only considers "horses" because it is the only candidate that lies in the top 70% of the probability distribution. If you set Top P as 0.9, the model considers "horses" and "zebras" as they are in the top 90% of probability distribution.

_______-

# Amazon SageMaker Data Wrangler

Amazon SageMaker Data Wrangler reduces the time it takes to aggregate and prepare tabular and image data for ML from weeks to minutes. With SageMaker Data Wrangler, you can simplify the process of data preparation and feature engineering, and complete each step of the data preparation workflow (including data selection, cleansing, exploration, visualization, and processing at scale) from a single visual interface. You can use SQL to select the data that you want from various data sources and import it quickly. Next, you can use the data quality and insights report to automatically verify data quality and detect anomalies, such as duplicate rows and target leakage. SageMaker Data Wrangler contains over 300 built-in data transformations, so you can quickly transform data without writing code.

With the SageMaker Data Wrangler data selection tool, you can quickly access and select your tabular and image data from various popular sources - such as Amazon Simple Storage Service (Amazon S3), Amazon Athena, Amazon Redshift, AWS Lake Formation, Snowflake, and Databricks - and over 50 other third-party sources - such as Salesforce, SAP, Facebook Ads, and Google Analytics. You can also write queries for data sources using SQL and import data directly into SageMaker from various file formats, such as CSV, Parquet, JSON, and database tables.

# SageMaker Model Dashboard

Amazon SageMaker Model Dashboard is a centralized portal, accessible from the SageMaker console, where you can view, search, and explore all of the models in your account. You can track which models are deployed for inference and if they are used in batch transform jobs or hosted on endpoints.

# Amazon SageMaker Clarify 

 SageMaker Clarify helps identify potential bias during data preparation without writing code. You specify input features, such as gender or age, and SageMaker Clarify runs an analysis job to detect potential bias in those features.

# Amazon SageMaker Feature Store 
Amazon SageMaker Feature Store is a fully managed, purpose-built repository to store, share, and manage features for machine learning (ML) models. Features are inputs to ML models used during training and inference.

# AWS Audit Manager

AWS Audit Manager helps automate the collection of evidence to continuously audit your AWS usage. It simplifies the process of assessing risk and compliance with regulations and industry standards, making it an essential tool for governance in AI systems.



# AWS Artifact - 

AWS Artifact provides on-demand access to AWS’ compliance reports and online agreements. It is useful for obtaining compliance documentation but does not provide continuous auditing or automated evidence collection.

# AWS Trusted Advisor -

 AWS Trusted Advisor offers guidance to help optimize your AWS environment for cost savings, performance, security, and fault tolerance. While it provides recommendations for best practices, it does not focus on auditing or evidence collection for compliance.

# AWS CloudTrail - 

AWS CloudTrail records AWS API calls for auditing purposes and delivers log files for compliance and operational troubleshooting. It is crucial for tracking user activity but does not automate compliance assessments or evidence collection.

# Ways to reduce high bias in Machine Learning:
Use a more complex model: One of the main reasons for high bias is the very simplified model. it will not be able to capture the complexity of the data. In such cases, we can make our mode more complex by increasing the number of hidden layers in the case of a deep neural network. Or we can use a more complex model like Polynomial regression for non-linear datasets, CNN for image processing, and RNN for sequence learning.
Increase the number of features: By adding more features to train the dataset will increase the complexity of the model. And improve its ability to capture the underlying patterns in the data.
Reduce Regularization of the model: Regularization techniques such as L1 or L2 regularization can help to prevent overfitting and improve the generalization ability of the model. if the model has a high bias, reducing the strength of regularization or removing it altogether can help to improve its performance.
Increase the size of the training data: Increasing the size of the training data can help to reduce bias by providing the model with more examples to learn from the dataset.

# BEDROCK

## Knowledge Bases for Amazon Bedrock

With Knowledge Bases for Amazon Bedrock, you can give FMs and agents contextual information from your company’s private data sources for RAG to deliver more relevant, accurate, and customized responses

Knowledge Bases for Amazon Bedrock takes care of the entire ingestion workflow of converting your documents into embeddings (vector) and storing the embeddings in a specialized vector database. Knowledge Bases for Amazon Bedrock supports popular databases for vector storage, including vector engine for Amazon OpenSearch Serverless, Pinecone, Redis Enterprise Cloud, Amazon Aurora (coming soon), and MongoDB (coming soon). If you do not have an existing vector database, Amazon Bedrock creates an OpenSearch Serverless vector store for you.

## Watermark detection for Amazon Bedrock

 The watermark detection mechanism allows you to identify images generated by Amazon Titan Image Generator, a foundation model that allows users to create realistic, studio-quality images in large volumes and at low cost, using natural language prompts. With watermark detection, you can increase transparency around AI-generated content by mitigating harmful content generation and reducing the spread of misinformation. You cannot use a watermark detection mechanism to implement RAG workflow in Amazon Bedrock.

# Continued pretraining in Amazon Bedrock 

 In the continued pretraining process, you provide unlabeled data to pre-train a model by familiarizing it with certain types of inputs. You can provide data from specific topics to expose a model to those areas. The continued pretraining process will tweak the model parameters to accommodate the input data and improve its domain knowledge. You can use continued pretraining or fine-tuning for model customization in Amazon Bedrock. You cannot use continued pretraining to implement RAG workflow in Amazon Bedrock.

# Guardrails for Amazon Bedrock 

Guardrails for Amazon Bedrock help you implement safeguards for your generative AI applications based on your use cases and responsible AI policies. It helps control the interaction between users and FMs by filtering undesirable and harmful content, redacts personally identifiable information (PII), and enhances content safety and privacy in generative AI applications. You cannot use guardrails to implement RAG workflow in Amazon Bedrock.

# Key terminology Bedrock.

- Foundation model (FM) – An AI model with a large number of parameters and trained on a massive amount of diverse data. A foundation model can generate a variety of responses for a wide range of use cases. Foundation models can generate text or image, and can also convert input into embeddings. Before you can use an Amazon Bedrock foundation model, you must request access. For more information about foundation models, see Supported foundation models in Amazon Bedrock.

- Base model – A foundation model that is packaged by a provider and ready to use. Amazon Bedrock offers a variety of industry-leading foundation models from leading providers. For more information, see Supported foundation models in Amazon Bedrock.

- Model inference – The process of a foundation model generating an output (response) from a given input (prompt). For more information, see Submit prompts and generate responses with model inference.

- Prompt – An input provided to a model to guide it to generate an appropriate response or output for the input. For example, a text prompt can consist of a single line for the model to respond to, or it can detail instructions or a task for the model to perform. The prompt can contain the context of the task, examples of outputs, or text for a model to use in its response. Prompts can be used to carry out tasks such as classification, question answering, code generation, creative writing, and more. For more information, see Prompt engineering concepts.

- Token – A sequence of characters that a model can interpret or predict as a single unit of meaning. For example, with text models, a token could correspond not just to a word, but also to a part of a word with grammatical meaning (such as "-ed"), a punctuation mark (such as "?"), or a common phrase (such as "a lot").

- Model parameters – Values that define a model and its behavior in interpreting input and generating responses. Model parameters are controlled and updated by providers. You can also update model parameters to create a new model through the process of model customization.

- Inference parameters – Values that can be adjusted during model inference to influence a response. Inference parameters can affect how varied responses are and can also limit the length of a response or the occurrence of specified sequences. For more information and definitions of specific inference parameters, see Influence response generation with inference parameters.

- Playground – A user-friendly graphical interface in the AWS Management Console in which you can experiment with running model inference to familiarize yourself with Amazon Bedrock. Use the playground to test out the effects of different models, configurations, and inference parameters on the responses generated for different prompts that you enter. For more information, see Generate responses in the console using playgrounds.

- Embedding – The process of condensing information by transforming input into a vector of numerical values, known as the embeddings, in order to compare the similarity between different objects by using a shared numerical representation. For example, sentences can be compared to determine the similarity in meaning, images can be compared to determine visual similarity, or text and image can be compared to see if they're relevant to each other. You can also combine text and image inputs into an averaged embeddings vector if it's relevant to your use case. For more information, see Submit prompts and generate responses with model inference and Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases.

- Orchestration – The process of coordinating between foundation models and enterprise data and applications in order to carry out a task. For more information, see Automate tasks in your application using AI agents.

- Agent – An application that carries out orchestrations through cyclically interpreting inputs and producing outputs by using a foundation model. An agent can be used to carry out customer requests. For more information, see Automate tasks in your application using AI agents.

- Retrieval augmented generation (RAG) – The process involves:

    - Querying and retrieving information from a data source
     
    - Augmenting a prompt with this information to provide better context to the foundation model
    
    - Obtaining a better response from the foundation model using the additional context

For more information, see Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases.

- Model customization – The process of using training data to adjust the model parameter values in a base model in order to create a custom model. Examples of model customization include Fine-tuning, which uses labeled data (inputs and corresponding outputs), and Continued Pre-training, which uses unlabeled data (inputs only) to adjust model parameters. For more information about model customization techniques available in Amazon Bedrock, see Customize your model to improve its performance for your use case.

- Hyperparameters – Values that can be adjusted for model customization to control the training process and, consequently, the output custom model. For more information and definitions of specific hyperparameters, see Custom model hyperparameters.

- Model evaluation – The process of evaluating and comparing model outputs in order to determine the model that is best suited for a use case. For more information, see Evaluate the performance of Amazon Bedrock resources.

- Provisioned Throughput – A level of throughput that you purchase for a base or custom model in order to increase the amount and/or rate of tokens processed during model inference. When you purchase Provisioned Throughput for a model, a provisioned model is created that can be used to carry out model inference. For more information, see Provisioned Throughput.

https://docs.aws.amazon.com/bedrock/latest/userguide/key-definitions.html 


# Model Inference vs Model evaluation

Model evaluation is the process of evaluating and comparing model outputs to determine the model that is best suited for a use case, whereas, model inference is the process of a model generating an output (response) from a given input (prompt)

# underfitting vs overfitting

underfitting, where the model fails to capture the underlying patterns in the data, resulting in poor performance on both training and new data - Underfitting happens when a model is too simple to learn the complexities of the data, leading to poor performance on both training and unseen datasets. While underfitting does cause incorrect responses, it is due to the model's inability to learn from data

overfitting, where the model performs exceptionally well on the training data but fails to generalize to new, unseen data - Overfitting occurs when a model learns the training data too well, capturing noise or irrelevant details, which results in poor performance on new data. 

## ¿Qué es Overfitting (sobreajuste)?
Definición:

El overfitting ocurre cuando un modelo de IA (por ejemplo, una red neuronal, un árbol de decisión o un modelo de regresión) aprende demasiado bien los datos de entrenamiento, incluyendo el ruido, errores o peculiaridades que no representan el patrón general del problema.

En otras palabras:
➡️ El modelo tiene un rendimiento excelente en los datos de entrenamiento, pero fracasa al generalizar a datos nuevos (de prueba o del mundo real).

Síntomas comunes:

Error muy bajo en entrenamiento, pero alto en validación o prueba.

Curva de aprendizaje donde la pérdida de entrenamiento sigue bajando, pero la de validación sube.

Predicciones que son muy precisas solo para los datos vistos, pero erráticas para nuevos.

Ejemplo:

Supón que entrenas un modelo para predecir el precio de casas y le das los datos de 1000 casas.
El modelo aprende incluso detalles como “esta casa tenía una puerta roja y costó más”.
Eso no es un patrón general, pero el modelo lo memoriza.

Resultado:

Entrenamiento: precisión 99%.

Datos nuevos: precisión 65%.
👉 Está sobreajustado.

Causas típicas:

Modelo demasiado complejo (muchos parámetros, muchas capas, profundidad excesiva).

Pocos datos de entrenamiento.

Falta de regularización (no se penaliza la complejidad).

Entrenamiento por demasiadas épocas.

Soluciones comunes:

Regularización: L1, L2, dropout, early stopping.

Más datos: aumentar tamaño y diversidad del dataset.

Reducir la complejidad del modelo.

Validación cruzada (cross-validation): evaluar mejor la generalización.

⚙️ 2. ¿Qué es Underfitting (subajuste)?
Definición:

El underfitting ocurre cuando el modelo no logra aprender los patrones importantes del conjunto de datos, es decir, ni siquiera se ajusta bien al entrenamiento.

➡️ El modelo es demasiado simple para capturar la complejidad del problema.

Síntomas comunes:

Alto error en entrenamiento y en validación.

Las curvas de aprendizaje muestran poca mejora aunque se entrene más.

Predicciones pobres en todos los casos.

Ejemplo:

Si intentas predecir el precio de casas con un modelo lineal simple usando solo un parámetro (por ejemplo, el número de habitaciones), pero el precio también depende de la ubicación, tamaño, antigüedad, etc.,
entonces el modelo no tiene suficiente capacidad.

Resultado:

Entrenamiento: precisión 60%.

Validación: precisión 58%.
👉 Está subajustado.

Causas típicas:

Modelo demasiado simple.

Demasiadas restricciones o regularización excesiva.

Muy pocos parámetros o características.

Entrenamiento insuficiente (pocas épocas).

Soluciones comunes:

Aumentar la complejidad del modelo: más capas, más parámetros, modelos no lineales.

Más entrenamiento: más épocas o menor tasa de aprendizaje.

Eliminar regularización excesiva.

Agregar características relevantes (feature engineering).

📈 3. Comparación directa
Aspecto	Underfitting	Overfitting
Error en entrenamiento	Alto	Muy bajo
Error en validación	Alto	Alto
Complejidad del modelo	Muy baja	Muy alta
Generalización	Mala (no aprende)	Mala (memoriza)
Solución	Aumentar complejidad	Reducir complejidad o regularizar
🧠 4. Intuición visual (mental)

Imagina que tienes puntos en un gráfico (datos) y dibujas una línea que intenta ajustarlos:

Underfitting: una línea recta que no sigue la tendencia (demasiado simple).

Overfitting: una línea que zigzaguea pasando por cada punto (demasiado compleja).

Buen ajuste: una curva suave que sigue la tendencia general sin ajustarse al ruido.

# Diffusion Model (more used in images)

 Diffusion models create new data by iteratively making controlled random changes to an initial data sample. They start with the original data and add subtle changes (noise), progressively making it less similar to the original. This noise is carefully controlled to ensure the generated data remains coherent and realistic. After adding noise over several iterations, the diffusion model reverses the process. Reverse denoising gradually removes the noise to produce a new data sample that resembles the original.

# Generative adversarial network (GAN) 

GANs work by training two neural networks in a competitive manner. The first network, known as the generator, generates fake data samples by adding random noise. The second network, called the discriminator, tries to distinguish between real data and the fake data produced by the generator. During training, the generator continually improves its ability to create realistic data while the discriminator becomes better at telling real from fake. This adversarial process continues until the generator produces data that is so convincing that the discriminator can't differentiate it from real data.

# Variational autoencoders (VAE) 
VAEs use two neural networks—the encoder and the decoder. The encoder neural network maps the input data to a mean and variance for each dimension of the latent space. It generates a random sample from a Gaussian (normal) distribution. This sample is a point in the latent space and represents a compressed, simplified version of the input data. The decoder neural network takes this sampled point from the latent space and reconstructs it back into data that resembles the original input.

# Model Evaluation

Model evaluation refers to assessing the performance of a machine learning model using specific metrics such as accuracy, precision, recall, or F1 score.




# Decision Trees

Decision Trees are highly interpretable models that provide a clear and straightforward visualization of the decision-making process. Decision Trees work by splitting the data into subsets based on the most significant features, resulting in a tree-like structure where each branch represents a decision rule. This makes it easy to understand how different characteristics of movies contribute to the final classification, making Decision Trees the most suitable choice for this task. So, Decision Trees offer high interpretability and transparency, which aligns with the company's need to document the inner mechanisms of how the model affects the output.

 via - https://docs.aws.amazon.com/whitepapers/latest/model-explainability-aws-ai-ml/interpretability-versus-explainability.html



# Logistic Regression - 
Logistic Regression is primarily designed for binary classification problems. While it can be adapted for multiclass classification, it may not perform effectively with a large number of categories or a complex dataset like a massive movie database. Additionally, logistic regression does not provide an easily interpretable structure that illustrates how each feature influences the final output, making it less suitable for the company's requirements.

# Neural Networks 
 This option is incorrect because, although neural networks are powerful tools for handling large and complex datasets, they are often considered "black-box" models due to their lack of transparency. Neural networks involve multiple layers of neurons and nonlinear transformations, making it difficult to understand and document the inner workings of the model. Given the company’s need for transparency and an understanding of how the model affects the output, neural networks are not the best choice.

# Support Vector Machines (SVMs) 
 This option is incorrect because, while SVMs are effective for classification tasks, especially in high-dimensional spaces, they do not inherently provide an interpretable way to understand the decision-making process. SVMs create a hyperplane to separate classes, but it is not straightforward to explain how individual features impact the final classification. This lack of interpretability makes SVMs less suitable for a company that wants to document and understand the inner workings of the model.

 # Embedding
Embeddings are numerical representations of real-world objects that machine learning (ML) and artificial intelligence (AI) systems use to understand complex knowledge domains like humans do. As an example, computing algorithms understand that the difference between 2 and 3 is 1, indicating a close relationship between 2 and 3 as compared to 2 and 100. However, real-world data includes more complex relationships. For example, a bird-nest and a lion-den are analogous pairs, while day-night are opposite terms. Embeddings convert real-world objects into complex mathematical representations that capture inherent properties and relationships between real-world data. The entire process is automated, with AI systems self-creating embeddings during training and using them as needed to complete new tasks.



 ## Embedding models
 
 Embedding models are algorithms trained to encapsulate information into dense representations in a multi-dimensional space. Data scientists use embedding models to enable ML models to comprehend and reason with high-dimensional data. These are common embedding models used in ML applications.

### Principal component analysis 
Principal component analysis (PCA) is a dimensionality-reduction technique that reduces complex data types into low-dimensional vectors. It finds data points with similarities and compresses them into embedding vectors that reflect the original data. While PCA allows models to process raw data more efficiently, information loss may occur during processing.

### Singular value decomposition 
Singular value decomposition (SVD) is an embedding model that transforms a matrix into its singular matrices. The resulting matrices retain the original information while allowing models to better comprehend the semantic relationships of the data they represent. Data scientists use SVD to enable various ML tasks, including image compression, text classification, and recommendation. 

### Word2Vec
Word2Vec is an ML algorithm trained to associate words and represent them in the embedding space. Data scientists feed the Word2Vec model with massive textual datasets to enable natural language understanding. The model finds similarities in words by considering their context and semantic relationships.

There are two variants of Word2Vec—Continuous Bag of Words (CBOW) and Skip-gram. CBOW allows the model to predict a word from the given context, while Skip-gram derives the context from a given word. While Word2Vec is an effective word embedding technique, it cannot accurately distinguish contextual differences of the same word used to imply different meanings. 

### BERT
BERT is a transformer-based language model trained with massive datasets to understand languages like humans do. Like Word2Vec, BERT can create word embeddings from input data it was trained with. Additionally, BERT can differentiate contextual meanings of words when applied to different phrases. For example, BERT creates different embeddings for ‘play’ as in “I went to a play” and “I like to play.” 

# Inferences

## Asynchronous inference

Asynchronous inference is the most suitable choice for this scenario. It allows the company to process smaller payloads without requiring real-time responses by queuing the requests and handling them in the background. This method is cost-effective and efficient when some delay is acceptable, as it frees up resources and optimizes compute usage. Asynchronous inference is ideal for scenarios where the payload size is less than 1 GB and immediate results are not critical.

## Batch inference 
 Batch inference is generally used for processing large datasets all at once. While it does not require immediate responses, it is typically more efficient for handling larger payloads (several gigabytes or more). For smaller payloads of less than 1 GB, batch inference might be overkill and less cost-efficient compared to asynchronous inference.

## Real-time inference 
Real-time inference is optimized for scenarios where low latency is essential, and responses are needed immediately. It is not suitable for cases where the system can afford to wait for responses, as it might lead to higher costs and resource consumption without providing any additional benefit for this particular use case.

## Serverless inference 
Serverless inference is a good choice for workloads with unpredictable traffic or sporadic requests, as it scales automatically based on demand. However, it may not be as cost-effective for scenarios where workloads are predictable, and some waiting time is acceptable. Asynchronous inference provides a more targeted solution for handling delayed responses at a lower cost.

# Transformer-based models
The transformer-based generative AI model builds upon the encoder and decoder concepts of VAEs. Transformer-based models add more layers to the encoder to improve performance on text-based tasks like comprehension, translation, and creative writing.

Transformer-based models use a self-attention mechanism. They weigh the importance of different parts of an input sequence when processing each element in the sequence.

Another key feature is that these AI models implement contextual embeddings. The encoding of a sequence element depends not only on the element itself but also on its context within the sequence.

How transformer-based models work
To understand how transformer-based models work, imagine a sentence as a sequence of words.

Self-attention helps the model focus on the relevant words as it processes each word. The transformer-based generative model employs multiple encoder layers called attention heads to capture different types of relationships between words. Each head learns to attend to different parts of the input sequence, allowing the model to simultaneously consider various aspects of the data.

Each layer also refines the contextual embeddings, making them more informative and capturing everything from grammar syntax to complex semantic meanings.

# Confusion matrix

Confusion matrix is a tool specifically designed to evaluate the performance of classification models by displaying the number of true positives, true negatives, false positives, and false negatives. This matrix provides a detailed breakdown of the model's performance across all classes, making it the most suitable choice for evaluating a classification model's accuracy and identifying potential areas for improvement. It provides a comprehensive overview of the model's performance by detailing how many instances were correctly or incorrectly classified in each category. This enables the company to understand where the model is performing well and where it may need adjustments, such as improving the classification of specific material types.


# Root Mean Squared Error (RMSE) 
 Root Mean Squared Error (RMSE) is a metric commonly used to measure the average error in regression models by calculating the square root of the average squared differences between predicted and actual values. However, RMSE is not suitable for classification tasks, as it is designed to measure continuous outcomes, not discrete class predictions.

# Mean Absolute Error (MAE)
Mean Absolute Error (MAE) measures the average magnitude of errors in a set of predictions without considering their direction. MAE is typically used in regression tasks to quantify the accuracy of a continuous variable's predictions, not for classification tasks where the outputs are categorical rather than continuous.

# Correlation matrix
 Correlation matrix measures the statistical correlation between different variables or features in a dataset, typically used to understand the relationships between continuous variables. A correlation matrix is not designed to evaluate the performance of a classification model, as it does not provide any insight into the accuracy or errors of categorical predictions.

# Fine-tuning vs Continued pre-training

## Fine-tuning
Fine-tuning is the process of taking a pre-trained FM, such as Llama 2, and further training it on a downstream task with a dataset specific to that task. The pre-trained model provides general linguistic knowledge, and fine-tuning allows it to specialize and improve performance on a particular task like text classification, question answering, or text generation. With fine-tuning, you provide labeled datasets—which are annotated with additional context—to train the model on specific tasks. You can then adapt the model parameters for the specific task based on your business context.

You can implement fine-tuning on FMs with Amazon SageMaker JumpStart and Amazon Bedrock. For more details, refer to Deploy and fine-tune foundation models in Amazon SageMaker JumpStart with two lines of code and Customize models in Amazon Bedrock with your own data using fine-tuning and continued pre-training.

## Continued pre-training
Continued pre-training in Amazon Bedrock enables you to teach a previously trained model on additional data similar to its original data. It enables the model to gain more general linguistic knowledge rather than focus on a single application. With continued pre-training, you can use your unlabeled datasets, or raw data, to improve the accuracy of foundation model for your domain through tweaking model parameters. For example, a healthcare company can continue to pre-train its model using medical journals, articles, and research papers to make it more knowledgeable on industry terminology. For more details, refer to Amazon Bedrock Developer Experience.

## Model customization 

Model customization involves further training and changing the weights of the model to enhance its performance. You can use continued pre-training or fine-tuning for model customization in Amazon Bedrock.

In the continued pre-training process, you provide **unlabeled** data to pre-train a model by familiarizing it with certain types of inputs. You can provide data from specific topics to expose a model to those areas. The Continued Pre-training process will tweak the model parameters to accommodate the input data and improve its domain knowledge.

For example, you can train a model with private data, such as business documents, that are not publicly available for training large language models. Additionally, you can continue to improve the model by retraining the model with more unlabeled data as it becomes available.

While fine-tuning a model, you provide **labeled** data to train a model to improve performance on specific tasks. By providing a training dataset of labeled examples, the model learns to associate what types of outputs should be generated for certain types of inputs. The model parameters are adjusted in the process and the model's performance is improved for the tasks represented by the training dataset.

Continued pre-training uses unlabeled data to pre-train a model, whereas, fine-tuning uses labeled data to train a model

# Amazon q vs BEDROCK

Amazon Q is a generative AI–powered assistant that allows you to create pre-packaged generative AI applications, whereas, Amazon Bedrock provides an environment to build and scale generative AI applications using a Foundation Model (FM)

Amazon Q is a generative AI-powered assistant for accelerating software development and leveraging companies' internal data. Amazon Q generates code, tests, and debugs. It has multistep planning and reasoning capabilities that can transform and implement new code generated from developer requests. Amazon Q also makes it easier for employees to get answers to questions across business data.

Amazon Bedrock provides an environment to build and scale generative AI applications with FMs. It is a fully managed service that offers a choice of high-performing FMs from leading AI companies. It also provides a broad set of capabilities around security, privacy, and responsible AI. It also supports fine-tuning, Retrieval Augmented Generation (RAG), and agents that execute tasks.

With Amazon Bedrock, you can choose the underlying Foundation Model. However, Amazon Q does not allow you to choose the underlying Foundation Model

Amazon Bedrock offers a choice of high-performing Foundation Models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon through a single API. On the other hand, you cannot choose the underlying Foundation Model with Amazon Q.

# La evaluación de los modelos de IA

La evaluación de los modelos de IA es un proceso multifacético que depende en gran medida del tipo de modelo y su aplicación. Aquí te explico los aspectos clave:

# Métricas de Rendimiento
Las métricas son fundamentales para cuantificar qué tan bien se desempeña un modelo. Algunas de las más comunes incluyen:

- Precisión (Accuracy): Mide la proporción de predicciones correctas sobre el total de predicciones. Es útil para tareas de clasificación.
- Recall (Sensibilidad): Mide la proporción de verdaderos positivos que fueron identificados correctamente. Es importante cuando los falsos negativos son costosos (por ejemplo, en detección de enfermedades).
- Precisión (Precision): Mide la proporción de verdaderos positivos sobre el total de predicciones positivas. Es relevante cuando los falsos positivos son costosos (por ejemplo, en sistemas de recomendación).
- F1-Score: Es la media armónica de la precisión y el recall, ofreciendo un equilibrio entre ambas.
- AUC-ROC (Area Under the Receiver Operating Characteristic Curve): Evalúa la capacidad de un clasificador para distinguir entre clases. Un valor más alto indica un mejor rendimiento.
- Error Cuadrático Medio (MSE - Mean Squared Error): Comúnmente usado en regresión, mide el promedio de los cuadrados de los errores.
- Error Absoluto Medio (MAE - Mean Absolute Error): También para regresión, mide el promedio de los valores absolutos de los errores.
- Perplejidad: Utilizada en modelos de lenguaje, mide qué tan bien predice el modelo una muestra. Una perplejidad más baja indica un mejor modelo.

Conjuntos de Datos de Evaluación
Para una evaluación justa y robusta, los modelos se prueban en conjuntos de datos que no se utilizaron durante el entrenamiento. Esto ayuda a asegurar que el modelo no simplemente memorizó los datos de entrenamiento, sino que ha aprendido a generalizar.

- Conjunto de Entrenamiento: Datos utilizados para entrenar el modelo.
- Conjunto de Validación: Datos utilizados para ajustar los hiperparámetros del modelo y para la selección del modelo durante el entrenamiento.
- Conjunto de Prueba: Datos completamente nuevos y no vistos por el modelo, utilizados para la evaluación final del rendimiento.

Técnicas de Evaluación
Existen varias técnicas para evaluar modelos de IA:

- Validación Cruzada (Cross-Validation): Divide el conjunto de datos en múltiples subconjuntos. El modelo se entrena y evalúa varias veces, utilizando diferentes subconjuntos para entrenamiento y validación en cada iteración. Esto ayuda a obtener una estimación más robusta del rendimiento del modelo.
- Análisis de Errores: Implica examinar los casos en los que el modelo comete errores para entender sus limitaciones y áreas de mejora.
- Evaluación Humana: En muchos casos, especialmente en tareas de procesamiento de lenguaje natural o visión por computadora, la evaluación humana es crucial para juzgar la calidad de las salidas del modelo, ya que las métricas automáticas pueden no capturar todos los matices.
- Pruebas de Robustez y Adversarias: Se evalúa cómo se comporta el modelo ante entradas ligeramente modificadas o "adversarias" que están diseñadas para engañarlo. Esto es importante para la seguridad y fiabilidad del modelo.
- Análisis de Sesgos y Equidad: Se evalúa si el modelo muestra sesgos hacia ciertos grupos demográficos o si su rendimiento es equitativo en diferentes subgrupos de la población.

Consideraciones Adicionales
- Interpretabilidad y Explicabilidad (XAI): Cada vez más, se evalúa la capacidad de un modelo para explicar sus decisiones, lo cual es crucial en campos como la medicina o las finanzas.
- Eficiencia y Escalabilidad: Se evalúa el tiempo de inferencia del modelo, el uso de recursos computacionales y su capacidad para escalar a grandes volúmenes de datos.
- Despliegue y Monitoreo: Una vez que un modelo se despliega en producción, su rendimiento se monitorea continuamente para detectar cualquier degradación o cambio en el comportamiento.

# Decision Trees

Decision Trees are highly interpretable models that provide a clear and straightforward visualization of the decision-making process. Decision Trees work by splitting the data into subsets based on the most significant features, resulting in a tree-like structure where each branch represents a decision rule. This makes it easy to understand how different characteristics of movies contribute to the final classification, making Decision Trees the most suitable choice for this task. So, Decision Trees offer high interpretability and transparency, which aligns with the company's need to document the inner mechanisms of how the model affects the output.

 via - https://docs.aws.amazon.com/whitepapers/latest/model-explainability-aws-ai-ml/interpretability-versus-explainability.html


# Logistic Regression - 

Logistic Regression is primarily designed for binary classification problems. While it can be adapted for multiclass classification, it may not perform effectively with a large number of categories or a complex dataset like a massive movie database. Additionally, logistic regression does not provide an easily interpretable structure that illustrates how each feature influences the final output, making it less suitable for the company's requirements.

# Neural Networks 

This option is incorrect because, although neural networks are powerful tools for handling large and complex datasets, they are often considered "black-box" models due to their lack of transparency. Neural networks involve multiple layers of neurons and nonlinear transformations, making it difficult to understand and document the inner workings of the model. Given the company’s need for transparency and an understanding of how the model affects the output, neural networks are not the best choice.

# Support Vector Machines (SVMs) 

 This option is incorrect because, while SVMs are effective for classification tasks, especially in high-dimensional spaces, they do not inherently provide an interpretable way to understand the decision-making process. SVMs create a hyperplane to separate classes, but it is not straightforward to explain how individual features impact the final classification. This lack of interpretability makes SVMs less suitable for a company that wants to document and understand the inner workings of the model.


# Techniques: supervised vs. unsupervised learning

In machine learning, you teach a computer to make predictions, or inferences. First, you use an algorithm and example data to train a model. Then, you integrate your model into your application to generate inferences in real time and at scale. Supervised and unsupervised learning are two distinct categories of algorithms.


## Supervised learning
In supervised learning, you train the model with a set of input data and a corresponding set of paired labeled output data. The labeling is typically done manually. Next are some types of supervised machine learning techniques.

- Logistic regression
Logistic regression predicts a categorical output based on one or more inputs. Binary classification is when the output fits into one of two categories, such as yes or no and pass or fail. Multiple class classification is when the output fits into more than two categories, such as cat, dog, or rabbit.  An example of logistic regression is predicting whether a student will pass or fail a unit based on their number of logins to the courseware.

Read about logistic regression »

- Linear regression
Linear regression refers to supervised learning models that, based on one or more inputs, predict a value from a continuous scale. An example of linear regression is predicting a house price. You could predict a house’s price based on its location, age, and number of rooms, after you train a model on a set of historical sales training data with those variables.

Read about linear regression »

- Decision tree
The decision tree supervised machine learning technique takes some given inputs and applies an if-else structure to predict an outcome. An example of a decision tree problem is predicting customer churn. For example, if a customer doesn’t visit an application after signing up, the model might predict churn. Or if the customer accesses the application on multiple devices and the average session time is above a given threshold, the model might predict retention.

- Neural network
A neural network solution is a more complex supervised learning technique. To produce a given outcome, it takes some given inputs and performs one or more layers of mathematical transformation based on adjusting data weightings. An example of a neural network technique is predicting a digit from a handwritten image.

Read about neural networks »

## Unsupervised learning 
Unsupervised machine learning is when you give the algorithm input data without any labeled output data. Then, on its own, the algorithm identifies patterns and relationships in and between the data . Next are some types of unsupervised learning techniques.

- Clustering
The clustering unsupervised learning technique groups certain data inputs together, so they may be categorized as a whole. There are various types of clustering algorithms depending on the input data. An example of clustering is identifying different types of network traffic to predict potential security incidents.

- Association rule learning
Association rule learning techniques uncover rule-based relationships between inputs in a dataset. For example, the Apriori algorithm conducts market basket analysis to identify rules like coffee and milk often being purchased together.

- Probability density
Probability density techniques in unsupervised learning predict the likelihood or possibility of an output’s value being within range of what is considered normal for an input. For example, a temperature gauge in a server room typically records between a certain degree range. However, if it suddenly measures a low number based on the probability distribution, it may indicate equipment malfunction. 

- Dimensionality reduction
Dimensionality reduction is an unsupervised learning technique that reduces the number of features in a dataset. It’s often used to preprocess data for other machine learning functions and reduce complexity and overheads. For example, it may blur out or crop background features in an image recognition application.

# When to use: supervised vs. unsupervised learning
You can use supervised learning techniques to solve problems with known outcomes and that have labeled data available. Examples include email spam classification, image recognition, and stock price predictions based on known historical data.

You can use unsupervised learning for scenarios where the data is unlabeled and the objective is to discover patterns, group similar instances, or detect anomalies. You can also use it for exploratory tasks where labeled data is absent. Examples include organizing large data archives,  building recommendation systems, and grouping customers based on their purchasing behaviors.