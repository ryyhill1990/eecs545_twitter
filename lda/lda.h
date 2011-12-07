#include <vector>

using namespace std;

class Datapoint
{
    public:
        int category;
        vector<double> value;
        Datapoint(int category, vector<double> value)
            : category (category), value(value)
        {}
};

class LDA
{
    public:
        int num_categories;
        int num_dimensions;
        vector<double> priors;
        vector<vector<double> > means;
        vector<vector<double> > covarience;

        LDA(vector<Datapoint> datapoints, int num_categories, int num_dimensions)
            : num_categories(num_categories), num_dimensions(num_dimensions),
            priors(vector<double>(num_categories, 0.0)),
            means(vector<vector<double> >(num_categories, vector<double>(num_dimensions, 0.0f))),
            covarience(vector<vector<double> >(num_dimensions, vector<double>(num_dimensions, 0.0f)))
    {
        // Find priors and means
        for (vector<Datapoint>::iterator it = datapoints.begin();
                it != datapoints.end(); ++it)
        {
            Datapoint datapoint = *it;
            priors[datapoint.category] += 1.0;
            for (int i = 0; i < num_dimensions; ++i)
            {
                means[datapoint.category][i] += datapoint.value[i];
            }
        }
        for (int i = 0; i < num_categories; ++i)
        {
            // At this point, priors hasn't been normalized,
            // so the value at priors[category] is the number
            // of datapoints from that category.
            for (int j = 0; j < num_dimensions; ++j)
            {
                means[i][j] /= priors[i];
            }
        }

        // Find covarience
        for (vector<Datapoint>::iterator it = datapoints.begin();
                it != datapoints.end(); ++it)
        {
            Datapoint datapoint = *it;
            vector<double> normalized_value = datapoint.value;
            for (int i = 0; i < num_dimensions; ++i)
            {
                normalized_value[i] -= means[datapoint.category][i];
            }
            for (int i = 0; i < num_dimensions; ++i)
            {
                for (int j = 0; j < num_dimensions; ++j)
                {
                    // priors still hasn't been normalized
                    covarience[i][j] += normalized_value[i] * normalized_value[j] / priors[datapoint.category];
                }
            }
        }
        // Normalize the priors to sum to 1.0
        for (int i = 0; i < num_categories; ++i)
        {
            priors[i] /= double(datapoints.size());
        }
    }

    double classify(vector<double> test_x) {

    }
};
