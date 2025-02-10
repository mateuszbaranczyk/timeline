import { useState } from 'react';
import './App.css';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

interface ApiResponse {
  summary: string;
  content: string;
}

function App() {
  const [topic, setTopic] = useState<string>("");
  const [responseData, setResponseData] = useState<ApiResponse[] | null>(null);
  const [summaries, setSummaries] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTopic(e.target.value);
  };

  const sendRequest = async () => {
    const url = `http://127.0.0.1:8000/topic/${topic}`;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setResponseData(data);
      await processData(data);
      await processData(data);
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
      setError('Failed to fetch data');
      setResponseData(null);
    } finally {
      setLoading(false);
    }
  };

  const processData = async (data: ApiResponse[]) => {
    for (const item of data) {
      const content = item.content;
      const apiUrl = 'http://127.0.0.1:3000/summarize/';
      try {
        const apiResponse = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: content }),
        });
        if (!apiResponse.ok) {
          throw new Error('Network response was not ok');
        }
        const apiData = await apiResponse.json();
        setSummaries((prevSummaries) => [...prevSummaries, apiData.summary]);
      } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
      }
    }
  };

  return (
    <Container>
      <Form className="mt-3">
        <Row>
          <Col xs={8}>
            <Form.Control placeholder="Topic" type="text" value={topic} onChange={handleInputChange} />
          </Col>  
          <Col xs={4}>
            <Button variant="primary" type="button" onClick={sendRequest}>
              Find
            </Button>
          </Col>
        </Row>
      </Form>
      <Row className="mt-3">
            {summaries.length > 0 && (
              <div>
                <h3>Summaries:</h3>
                {summaries.map((summary, index) => (
                  <Col key={index} className='justify-content-center'>
                    <Card className="mx-auto mb-3">
                      <Card.Body>
                        <Card.Text>
                          {summary}
                        </Card.Text>
                      </Card.Body>
                    </Card>
                  </Col>
                ))}
              </div>
            )}
      </Row>
    </Container>
  )
}

export default App