package postprocessors

import (
	"context"
	"encoding/json"

	"github.com/obot-platform/tools/knowledge/pkg/datastore/types"
	"github.com/obot-platform/tools/knowledge/pkg/llm"
	vs "github.com/obot-platform/tools/knowledge/pkg/vectorstore/types"
)

const ContentFilterPostprocessorName = "content_filter"

type ContentFilterPostprocessor struct {
	Question string // Question about the content, that can be answered with yes or no
	Include  bool   // Whether to include or exclude the documents for which the answer is yes
	Model    llm.LLMConfig
}

var promptTemplate string = `You're an expert content analyst.
You're given a question about document contents and have to answer it with true or false.
No other option is allowed.

The question is: "{.question}"

The content is:
{.content}

--- End of Content ---
Reply only with {"result": <true-or-false>}. Do not include anything else in your response, just raw JSON without markdown syntax.`

type cfpResponse struct {
	Result bool `json:"result"`
}

func (c *ContentFilterPostprocessor) Transform(ctx context.Context, response *types.RetrievalResponse) error {
	m, err := llm.NewFromConfig(c.Model)
	if err != nil {
		return err
	}

	for i, resp := range response.Responses {
		var filteredDocs []vs.Document
		for _, doc := range resp.ResultDocuments {
			res, err := m.Prompt(ctx, promptTemplate, map[string]any{
				"question": c.Question,
				"content":  doc.Content,
			})
			if err != nil {
				return err
			}

			var resp cfpResponse
			err = json.Unmarshal([]byte(res), &resp)
			if err != nil {
				return err
			}

			if resp.Result == c.Include {
				filteredDocs = append(filteredDocs, doc)
			}
		}
		response.Responses[i].ResultDocuments = filteredDocs
	}
	return nil
}

func (c *ContentFilterPostprocessor) Name() string {
	return ContentFilterPostprocessorName
}
