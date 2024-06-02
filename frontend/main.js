document.addEventListener("DOMContentLoaded", (event) => {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const historyCloseBtn = document.querySelector(".history-close-btn");
    const chatbox = document.querySelector(".chatbox");
    const chatbotHistory = document.querySelector(".chatbot-history");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector(".chat-input span");

    let userMessage = null; // Variable to store user's message
    const inputInitHeight = chatInput.scrollHeight;

    const createChatLi = (message, className) => {
        // Create a chat <li> element with passed message and className
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", `${className}`);
        let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined"></span><p></p>`;
        chatLi.innerHTML = chatContent;
        chatLi.querySelector("p").textContent = message;
        return chatLi; // return chat <li> element
    }

    const generateResponse = (chatElement) => {
        //const API_URL = "http://localhost:5000/query";
        const API_URL = "https://dummyjson.com/test";
        const messageElement = chatElement.querySelector("p");
        const messageElementChild = document.createElement("span");

        // Define the properties and message for the API request
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ input: userMessage })
        }

        // Send POST request to API, get response and set the reponse as paragraph text
        fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
            data = {
                "response": {
                    "answer": "Die semantische Heterogenität wird unterstellt, dass es sich um die Unterschiede in Bedeutung, Interpretation und Art der Nutzung von Informationen handelt. Es ist damit das größte Problem für die automatische Wissensverarbeitung.",
                    "context": [
                        {
                            "metadata": {
                                "page": 44,
                                "pk": 450095517748168738,
                                "source": "data/1877_KE7.pdf",
                                "start_index": 0
                            },
                            "page_content": "9. Lösungen der Selbsttestaufgaben\n7.1 Was wird unter der semantischen Heterogenität verstanden?\nDie semantische Heterogenität die Unterschiede in Bedeutung, Interpretation und Art der\nNutzung, speziell von Informationen. Es ist damit das größte Problem für die\nautomatische Wissensverarbeitung.\n7.2 Nennen und erklären Sie die drei Konzepte der semantischen Heterogenität.\n·        Bei semantisch äquivalenten Konzepten  können sich etwa verschiedene Begriffe\nauf ein und dasselbe Konzept beziehen.\n·        Bei semantisch unabhängigen Konzepten  kann es zu Verständnisproblemen\nkommen, wenn der gleiche Begriff für unterschiedliche Konzepte verwendet wird.\n·        Bei semantisch abhängigen Konzepten  wird die Heterogenität anhand von\nGeneralisierung und Spezifizierung beschrieben.\n7.3 Erklären Sie den Begriff der Taxonomie.\nMit einer Taxonomie werden Mengen von Konzepten von kontrollierten Vokabularen\neines Themengebietes definiert und in eine hierarchische Beziehung gesetzt, um eine",
                            "type": "Document"
                        },
                        {
                            "metadata": {
                                "page": 44,
                                "pk": 450095517748170060,
                                "source": "data/1877_KE7.pdf",
                                "start_index": 0
                            },
                            "page_content": "9. Lösungen der Selbsttestaufgaben\n7.1 Was wird unter der semantischen Heterogenität verstanden?\nDie semantische Heterogenität die Unterschiede in Bedeutung, Interpretation und Art der\nNutzung, speziell von Informationen. Es ist damit das größte Problem für die\nautomatische Wissensverarbeitung.\n7.2 Nennen und erklären Sie die drei Konzepte der semantischen Heterogenität.\n·        Bei semantisch äquivalenten Konzepten  können sich etwa verschiedene Begriffe\nauf ein und dasselbe Konzept beziehen.\n·        Bei semantisch unabhängigen Konzepten  kann es zu Verständnisproblemen\nkommen, wenn der gleiche Begriff für unterschiedliche Konzepte verwendet wird.\n·        Bei semantisch abhängigen Konzepten  wird die Heterogenität anhand von\nGeneralisierung und Spezifizierung beschrieben.\n7.3 Erklären Sie den Begriff der Taxonomie.\nMit einer Taxonomie werden Mengen von Konzepten von kontrollierten Vokabularen\neines Themengebietes definiert und in eine hierarchische Beziehung gesetzt, um eine",
                            "type": "Document"
                        },
                        {
                            "metadata": {
                                "page": 6,
                                "pk": 450095517748168050,
                                "source": "data/1877_KE5.pdf",
                                "start_index": 1668
                            },
                            "page_content": "Heterogenitätsprobleme auf der strukturellen Ebene bereits ausdifferenzierte Lösungen\naus der Datenbank-Forschung. Sowohl die maschinelle Interpretation von Information als\nauch die Verarbeitung der Semantik befinden sich hingegen noch in einem frühen\nForschungsstadium. Deshalb soll im Folgenden vor allem dieser Aspekt besondereSelbsttestaufgabe 5.1\nWas ist ein Semantisches Netz und wozu wird es verwendet?",
                            "type": "Document"
                        },
                        {
                            "metadata": {
                                "page": 6,
                                "pk": 450095517748169372,
                                "source": "data/1877_KE5.pdf",
                                "start_index": 1668
                            },
                            "page_content": "Heterogenitätsprobleme auf der strukturellen Ebene bereits ausdifferenzierte Lösungen\naus der Datenbank-Forschung. Sowohl die maschinelle Interpretation von Information als\nauch die Verarbeitung der Semantik befinden sich hingegen noch in einem frühen\nForschungsstadium. Deshalb soll im Folgenden vor allem dieser Aspekt besondereSelbsttestaufgabe 5.1\nWas ist ein Semantisches Netz und wozu wird es verwendet?",
                            "type": "Document"
                        }
                    ],
                    "input": "Was wird unter der semantischen Heterogenität verstanden?"
                }
            }

            if (data.response?.context !== "undefined") {
                messageElementChild.innerHTML = "<br/><br/><b>Quellenangabe:</b><br/>";
                const metadataToDisplay = ["page", "source"];
                data.response.context.forEach((element, index) => {
                    messageElementChild.innerHTML += "<b>" + parseInt(index + 1) + ":  </b>";
                    for (const [key, value] of Object.entries(element.metadata)) {
                        if (metadataToDisplay.indexOf(key) > -1) {
                            messageElementChild.innerHTML += "<b>" + key + ":</b> " + value + "  ";
                        }
                    }
                    messageElementChild.innerHTML += "<hr>";
                });
                //messageElement.textContent = data.response.answer;
                //messageElement.appendChild(messageElementChild);
                
                const tempMessageElement = document.createElement("p");
                tempMessageElement.textContent = data.response.answer;
                tempMessageElement.appendChild(messageElementChild);

                textTypingEffect(messageElement, tempMessageElement.innerHTML, 30);

            }
        }).catch(() => {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Etwas ist schief gelaufen, probiere es noch einmal.";
        }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
    }

    const handleChat = () => {
        userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
        if (!userMessage) return;

        // Clear the input textarea and set its height to default
        chatInput.value = "";
        chatInput.style.height = `${inputInitHeight}px`;

        // Append the user's message to the chatbox
        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTo(0, chatbox.scrollHeight);

        setTimeout(() => {
            // Display "Thinking..." message while waiting for the response
            const incomingChatLi = createChatLi("Antwort wird gesucht...", "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
            setTimeout(() => {generateResponse(incomingChatLi);}, 600);
        }, 600);
    }

    chatInput.addEventListener("input", () => {
        // Adjust the height of the input textarea based on its content
        chatInput.style.height = `${inputInitHeight}px`;
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", (e) => {
        // If Enter key is pressed without Shift key and the window 
        // width is greater than 800px, handle the chat
        if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleChat();
        }
    });

    sendChatBtn.addEventListener("click", handleChat);
    closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));

    historyCloseBtn.addEventListener("click", () => {
        chatbotHistory.classList.toggle("show-chatbotHistory");
        document.body.classList.toggle("transite-content");
    });

    chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

    const textTypingEffect = (element, sentence, speed = 30) => {
        let index = 0;

        let timer = setInterval(function () {
            const char = sentence[index];

            if (char === '<') {
                index = sentence.indexOf('>', index);  // skip to greater-than
            }

            element.innerHTML = sentence.slice(0, index);
            chatbox.scrollTo(0, chatbox.scrollHeight);

            if (++index === sentence.length) {
                clearInterval(timer);
            }
        }, speed);
    }
});