const URL = document.defaultView.URL || document.defaultView.webkitURL
const videoFileInput = document.querySelector('#video-file');

const playSelectedFile = (event) => {
    assignSource(videoFileInput, 'video')

    const targetFileInput = document.querySelector('#target-file');
    assignSource(targetFileInput, '#target-subs')

    const targetLemmasFileInput = document.querySelector('#target-lemmas-file');
    assignSource(targetLemmasFileInput, '#target-lemmas')

    const translationFileInput = document.querySelector('#translation-file');
    assignSource(translationFileInput, '#translation-subs')
}

const assignSource = (sourceFile, sourceElementSelector) => {
    const file = sourceFile.files[0];
    const fileURL = URL.createObjectURL(file);
    const node = document.querySelector(sourceElementSelector);
    node.src = fileURL;
}

class Tracker {
    constructor(authService, url) {
        this.__authService = authService
        this.__url = url
        this.__video = document.querySelector('video')

        this.__sourceLanguage = ""
        this.__supportLanguage = ""

        const tracks = document.querySelector("video").textTracks;
        this.__track = tracks[0]
        this.__lemmasTrack = tracks[1]
        this.__translatedTrack = tracks[2]

        this.__playing = false
        this.__lastRevealed = ""
        this.__lastLemmas = []
        this.__lastTranslationRevealed = ""

        this.track = this.track.bind(this);
        this.toggleTracks = this.toggleTracks.bind(this);
    }

    __parseLanguages() {
        this.__sourceLanguage = document.querySelector('#sourceLanguage').value
        this.__supportLanguage = document.querySelector('#supportLanguage').value
    }

    __setInitialTrackModes() {
        this.__track.mode = "showing"
        this.__lemmasTrack.mode = "hidden"
        this.__translatedTrack.mode = "hidden"

    }

    __trackTranslationReveal(){

        document.addEventListener("keydown", (event) => {
            // Pressing '.' reveals translation track, only when the video is paused.
            // Reveal translation, store cue's contents, send an event.

            if (this.__playing) return;

            if (this.__track.activeCues) {
                if (event.keyCode === 190) {
                    this.toggleTracks();
                    if (this.__lastTranslationRevealed !== this.__lastRevealed) {
                        this.__dispatchTranslationWasRevealed()
                        this.__lastTranslationRevealed = this.__lastRevealed
                    }
                }
            }
        })
    }

    __dispatchTranslationWasRevealed() {
        console.log("VIDEO__TRANSLATION_WAS_REVEALED", this.__lastLemmas)
        this.__dispatch({
            message: 'VIDEO__TRANSLATION_WAS_REVEALED',
            lemmas: this.__lastLemmas,
            source_language: this.__sourceLanguage,
            support_language: this.__supportLanguage,
        })
    }

    __trackCueChange() {
        this.__track.addEventListener('cuechange', _ => {
            // Send events when captions seen and not translated.

            if (this.__lastRevealed && this.__lastRevealed !== this.__lastTranslationRevealed) {
                this.__dispatchWasSeen();
                this.__lastRevealed = "";
            }
            if (this.__track.activeCues.length) {
                this.__lastRevealed = this.__track.activeCues[0].text
                this.__lastLemmas = this.__lemmasTrack.activeCues[0].text.split(',')
            }
        })

    }

    __dispatchWasSeen() {
        console.log("VIDEO__WAS_SEEN", this.__lastLemmas);
        this.__dispatch({
            message: 'VIDEO__WAS_SEEN',
            lemmas: this.__lastLemmas,
            source_language: this.__sourceLanguage,
            support_language: this.__supportLanguage,
        })
    }

    track() {
        this.__parseLanguages()
        this.__setInitialTrackModes()

        this.__video.addEventListener('pause', _ => {
            this.__playing = false;
        })

        this.__video.addEventListener('play', _ => {
            this.__playing = true;
            this.__track.mode = "showing"
            this.__translatedTrack.mode = "hidden"
        })

        this.__trackTranslationReveal()
        this.__trackCueChange()

    }

    __dispatch(data) {
        return this.__authService.jwtPost(this.__url, data)
    }

    toggleTracks = () => {
        this.__track.mode = this.__track.mode === "showing" ? "hidden" : "showing"
        this.__translatedTrack.mode = this.__translatedTrack.mode === "showing" ? "hidden" : "showing"
    }
}

