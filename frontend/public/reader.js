class ReadingDocumentController {

    constructor(documentElement) {
        // First, let's keep the iframe pointer
        this.frame = documentElement

        // We will use the following as state:
        this.lookedUpWord = ""
        this.currentSentence = {
            supportText: "",
            tokensToLemmas: {}
        }

        // Custom events which are emitted by the frame.
        this.wordWasSelected =
            new CustomEvent('wordWasSelected', {
                bubbles: true,
                detail: () => this.lookedUpWord
            })
        this.sentenceWasClicked =
            new CustomEvent('sentenceWasClicked', {
                bubbles: true,
                detail: () => this.currentSentence
            })
        this.sentenceWasExposed =
            new CustomEvent('sentenceWasExposed', {
                bubbles: true,
                detail: () => this.currentSentence
            })

        // The rest is just binding class methods to this state.
        this.load = this.load.bind(this)
        this.__addStyles = this.__addStyles.bind(this)
        this.__frameWasLoaded = this.__frameWasLoaded.bind(this)
        this.getFrame = this.getFrame.bind(this)
        this.__addSentenceClickListeners = this.__addSentenceClickListeners.bind(this)
        this.__addIntersectionObserver = this.__addIntersectionObserver.bind(this)
        this.__outOfViewCallback = this.__outOfViewCallback.bind(this)
        this.__getDualLanguageChunks = this.__getDualLanguageChunks.bind(this)
        this.__parseLanguages = this.__parseLanguages.bind(this)
    }

    getFrame() {
        return this.frame
    }

    async load() {
        const url = this.__getAddress()
        return new Promise((resolve, reject) => {
            this.__fetch_document_as_blob(url)
                .then(blob => {
                    this.frame.src = blob
                    this.frame.onload = _ => {
                        this.__frameWasLoaded();
                        resolve()
                    }
                })
        })
    }

    async __frameWasLoaded(_) {
        this.__parseLanguages()
        this.__addStyles()
        this.__addSpaceAtBottom()
        this.__addSentenceClickListeners()
        this.__addWordSelectionListeners()
        this.__addIntersectionObserver()
    }

    __parseLanguages() {
        const head = this.frame.contentDocument.head
        this.languages = {
            sourceLanguage: head.querySelector('meta[name=source-language]').getAttribute('value'),
            supportLanguage: head.querySelector('meta[name=support-language]').getAttribute('value')
        }
    }

    getLanguages(){return this.languages;}

    __addStyles() {
        const doc = this.frame.contentDocument;
        this.__setReadableWidthWrapper(doc)
        this.__appendStylesheet(doc)

    }

    __setReadableWidthWrapper(doc) {
        const original_content = doc.body.innerHTML
        doc.body.innerHTML = `<div class='readable-width'>${original_content}</div>`
    }

    __appendStylesheet(doc) {
        const cssLink = document.createElement("link");
        cssLink.href = 'http://localhost:3000/reader.css';
        cssLink.rel = "stylesheet";
        cssLink.type = "text/css";
        doc.head.appendChild(cssLink);
    }

    __addSpaceAtBottom() {
        const div = document.createElement('div')
        div.classList.add('space-under')
        this.getFrame().contentDocument.body.appendChild(div)
    }

    __addSentenceClickListeners() {
        const spans = this.__getDualLanguageChunks()
        spans.forEach(span => {
            span.addEventListener('click', e => {
                this.currentSentence = {...this.__parseSpanDataset(span)}
                this.frame.dispatchEvent(this.sentenceWasClicked)
                span.classList.add('looked-up')
            })

        })
    }

    __getDualLanguageChunks() {
        return this.frame.contentDocument.querySelectorAll('span.dual-language-chunk')
    }

    __addWordSelectionListeners() {
        const matchesPunctuation = /[^A-Za-zÁÀȦÂÄǞǍĂĀÃÅǺǼǢĆĊĈČĎḌḐḒÉÈĖÊËĚĔĒẼE̊ẸǴĠĜǦĞG̃ĢĤḤáàȧâäǟǎăāãåǻǽǣćċĉčďḍḑḓéèėêëěĕēẽe̊ẹǵġĝǧğg̃ģĥḥÍÌİÎÏǏĬĪĨỊĴĶǨĹĻĽĿḼM̂M̄ʼNŃN̂ṄN̈ŇN̄ÑŅṊÓÒȮȰÔÖȪǑŎŌÕȬŐỌǾƠíìiîïǐĭīĩịĵķǩĺļľŀḽm̂m̄ŉńn̂ṅn̈ňn̄ñņṋóòôȯȱöȫǒŏōõȭőọǿơP̄ŔŘŖŚŜṠŠȘṢŤȚṬṰÚÙÛÜǓŬŪŨŰŮỤẂẀŴẄÝỲŶŸȲỸŹŻŽẒǮp̄ŕřŗśŝṡšşṣťțṭṱúùûüǔŭūũűůụẃẁŵẅýỳŷÿȳỹźżžẓǯßœŒçÇ]/
        const lookup_word = e => {
            const selection = this.frame.contentDocument.getSelection().toString();      // get the selection then
            if (selection.length < 2 || matchesPunctuation.test(selection)) {
                return
            }
            if (selection in this.currentSentence.tokensToLemmas) {
                const lemma = this.currentSentence.tokensToLemmas[selection]
                this.lookedUpWord = lemma
                this.frame.dispatchEvent(this.wordWasSelected)
            }
        }
        this.frame.contentDocument.body.addEventListener('mouseup', lookup_word)
    }

    __addIntersectionObserver() {
        let options = {
            root: this.frame.contentDocument,
            rootMargin: '0px 0px -100%',
            threshold: 0
        }
        const observer = new IntersectionObserver(this.__outOfViewCallback, options);
        const spans = this.__getDualLanguageChunks()
        spans.forEach(element => observer.observe(element));
    }


    __outOfViewCallback(entries) {
        if (!this.__outOfViewCallbackWasRun) this.__outOfViewCallbackWasRun = true;
        else entries.forEach((entry) => {
            if (this.__notSeen(entry.target)) {
                this.currentSentence = {...this.__parseSpanDataset(entry.target)}
                this.frame.dispatchEvent(this.sentenceWasExposed)
                entry.target.classList.add('exposed')
            }
        })
    }

    __parseSpanDataset(span) {
        return {
            supportText: JSON.parse(span.dataset.supportText),
            tokensToLemmas: JSON.parse(span.dataset.tokensToLemmas)
        }
    }

    __notSeen(element) {
        return !this.__isExposed(element) && !this.__isLookedUp(element)
    }

    __isExposed(element) {
        return element.classList.contains('exposed')
    }

    __isLookedUp(element) {
        return element.classList.contains('looked-up')
    }


    __getAddress() {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        return JSON.parse(urlParams.get('open'))
    }

    __fetch_document_as_blob(url){
        const xhr = new XMLHttpRequest();
        return new Promise((resolve, reject) => {
            xhr.responseType = 'blob';
            xhr.onreadystatechange = function () {
                if (this.readyState === this.DONE) {
                    if (this.status === 200) {
                        resolve(URL.createObjectURL(this.response))
                    } else {
                        reject(xhr);
                    }
                }
            }
            xhr.open('GET', url);
            xhr.setRequestHeader('Authorization', AuthService.jwtBearerToken());
            xhr.send();
        });
    }
}


class DefinitionController {
    constructor(sourceLanguageCode, supportLanguageCode, view) {
        this.view = view
        this.changeDefinition = this.changeDefinition.bind(this)
        this.sourceLanguage = this.__intlCodeToWord(sourceLanguageCode)
        this.supportLanguage = this.__intlCodeToWord(supportLanguageCode)
    }

    changeDefinition(newWord) {
        const uri= `http://www.linguee.com/${this.supportLanguage.toLowerCase()}-${this.sourceLanguage.toLowerCase()}/search?qe=${encodeURI(newWord)}&source=auto&cw=714&ch=398`
        console.log(uri)
        this.view.src = uri
    }

    __intlCodeToWord(code){
        const dict = {
            es:'Spanish',
            en:'English',
            zh:'Chinese',
            de:'German',
        }
        return dict[code]
    }
}


class SupportTextController {
    constructor(view) {
        this.view = view
        this.changeSupportText = this.changeSupportText.bind(this)
    }

    changeSupportText(newSupportText) {
        this.view.innerHTML = newSupportText
    }
}


class InteractionTracker {

    constructor(url, sourceLanguage,supportLanguage) {
        this.url                = url
        this.sourceLanguage     = sourceLanguage
        this.supportLanguage    = supportLanguage


        this.lemmaWasSelected = this.lemmaWasSelected.bind(this)
        this.sentenceWasClicked = this.sentenceWasClicked.bind(this)
        this.sentenceWasExposed = this.sentenceWasExposed.bind(this)
        this.__dispatch = this.__dispatch.bind(this)
    }

    lemmaWasSelected(lemma) {
        const data = InteractionTracker.__lemmaWasSelectedMessage(lemma,this.sourceLanguage, this.supportLanguage)
        return this.__dispatch(data)
    }

    sentenceWasClicked(lemmas) {
        const data = InteractionTracker.__sentenceWasClickedMessage(lemmas, this.sourceLanguage, this.supportLanguage)
        return this.__dispatch(data)
    }

    sentenceWasExposed(lemmas) {
        const data = InteractionTracker.__sentenceWasExposedMessage(lemmas, this.sourceLanguage, this.supportLanguage)
        return this.__dispatch(data)
    }

    __dispatch(data) {
        return AuthService.jwtPost(this.url, data)
    }

    static __lemmaWasSelectedMessage(lemma, sourceLanguage, supportLanguage) {
        return {
            message: 'TEXT__WORD_HIGHLIGHTED',
            lemmas: [lemma],
            source_language: sourceLanguage,
            support_language: supportLanguage,
        }
    }

    static __sentenceWasClickedMessage(lemmas,sourceLanguage, supportLanguage) {
        return {
            message: 'TEXT__SENTENCE_CLICK',
            lemmas: lemmas,
            source_language: sourceLanguage,
            support_language: supportLanguage,
        }
    }

    static __sentenceWasExposedMessage(lemmas,sourceLanguage, supportLanguage) {
        return {
            message: 'TEXT__SENTENCE_READ',
            lemmas: lemmas,
            source_language: sourceLanguage,
            support_language: supportLanguage,
        }
    }
}
