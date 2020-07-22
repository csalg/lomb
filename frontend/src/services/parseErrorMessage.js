export default function parseErrorMessage(error) {
    if (error.response) {
        if (error.response.data) {
            if (error.response.data.error)
                return error.response.data.error
        }
    } else
        return `Error connecting to backend:${JSON.stringify(error)}`
}
