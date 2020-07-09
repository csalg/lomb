class LemmasController {
    constructor(url) {
        this.currentLemma = {}
        this.examples = {}

        this.lemmaWasClickedEvent = new CustomEvent('lemmaWasClicked', {
            detail: () => this.currentLemma,
            bubbles: true
        })

        this.lemmaWasExposedEvent = new CustomEvent('lemmaWasExposed', {
            detail: () => this.currentLemma,
            bubbles: true
        })

        this.observer = this.__createObserver()

        this.__populateLemmasToExamples = this.__populateLemmasToExamples.bind(this)
        this.__createObserver = this.__createObserver.bind(this)
        this.__outOfViewCallback = this.__outOfViewCallback.bind(this)
        this.__observeLemmas = this.__observeLemmas.bind(this)

        this.__fetchLemmas(url)
            .then(lemmas => {
                this.__renderLemmas(lemmas)
                this.__populateLemmasToExamples(lemmas)
                this.__observeLemmas()
            })
    }

    __createObserver() {
        const options = {
            root: document.body,
            rootMargin: '0px 0px -100%',
            threshold: 0
        }
        this.firstRun = true
        return new IntersectionObserver(this.__outOfViewCallback(), options)
    }

    __outOfViewCallback() {
        return (entries) => {
            if (this.firstRun) {
                this.firstRun = false;
                return
            }
            if (entries.length > 20) {
                return
            }
            entries.forEach(entry => {
                    if (LemmasController.__isNotSeenBefore(entry.target)) {
                        entry.target.classList.add('exposed');
                        const lemmaName = entry.target.querySelector('.lemma-name').innerText
                        const sourceLanguage = entry.target.querySelector('.lemma-language').innerText
                        this.currentLemma = {
                            lemma: lemmaName,
                            language: sourceLanguage,
                            examples: this.examples[sourceLanguage][lemmaName]
                        }
                        document.body.dispatchEvent(this.lemmaWasExposedEvent)
                    }
                }
            )
        }
    }


    __fetchLemmas(url) {
        // eslint-disable-next-line no-undef
        return AuthService.jwtGet(url).then(e => e.json())
    }

    __renderLemmas(lemmas) {
        const tbody = document.querySelector('tbody')
        const template = document.querySelector('template#lemma')

        for (const i in lemmas) {
            const clone = template.content.cloneNode(true)
            clone.querySelector('td.lemma-name').textContent = lemmas[i].lemma
            clone.querySelector('td.lemma-language').textContent = lemmas[i].language
            clone.querySelector('td.lemma-frequency').textContent = lemmas[i].examples.length
            const tr = clone.querySelector('tr')
            tr.addEventListener('click', e => {
                this.currentLemma = lemmas[i];
                if (LemmasController.__isNotSeenBefore(e.target)) {
                    document.body.dispatchEvent(this.lemmaWasClickedEvent)
                    tr.classList.add('clicked')
                }
            })
            tbody.appendChild(clone)
        }
    }

    __populateLemmasToExamples(lemmas) {
        for (const i in lemmas) {
            const {lemma, language} = lemmas[i]
            if (!(language in this.examples)) {
                this.examples[language] = {}
            }
            this.examples[language][lemma] = lemmas[i]['examples']
        }

    }

    static __isNotSeenBefore(target) {
        return !(target.classList.contains('exposed') || target.classList.contains('clicked'))
    }

    __observeLemmas() {
        document.querySelectorAll('tbody>tr').forEach(
            tr => this.observer.observe(tr)
        )
    }
}