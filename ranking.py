# Define different preferences (weights) for 10 respondents
np.random.seed(42)  # For reproducibility
weights = np.random.uniform(0.5, 3.0, size=(10, 4))  # Increased weight range
weights = weights / weights.sum(axis=1, keepdims=True)  # Normalize to sum to 1

# Create a DataFrame to store priority weights
priority_weights = pd.DataFrame(weights, 
                                columns=['display_inch', 'camera', 'memory_gb', 'price_gbp'])
priority_weights.index = [f'Person_{i+1}' for i in range(10)]

# Rank Normalization for Attributes (Rank within each feature)

# Create a DataFrame to store priority weights
priority_weights = pd.DataFrame(weights, 
                                columns=['display_inch', 'camera', 'memory_gb', 'price_gbp'])
priority_weights.index = [f'Person_{i+1}' for i in range(10)]

# Generate rankings based on weighted scores
for i in range(10):
    # Add stronger random noise (5% of the score)
    noise = np.random.uniform(-0.05, 0.05, size=len(df_prod))
    
    # Calculate weighted score for each product combination
    scores = (
        weights[i][0] * (df_prod['display_inch'] / 2) +
        weights[i][1] * df_prod['camera'] +
        weights[i][2] * (df_prod['memory_gb'] / 100) +
        weights[i][3] * -(df_prod['price_gbp'] / 150)  +  # Lower price = better
        noise * np.max(df_prod['display_inch'])  # Scale noise to attribute level
    )
    
    # Rank scores (higher score = better ranking → rank 48 = best)
    df_prod['score'] = scores
    df_prod[f'respondent_{i + 1}'] = scores.rank(ascending=True).astype(int)
    
# Export the data    
df_prod = df_prod.drop(columns = ['score'])
df_prod.to_csv('product_survey.csv', index = False)
