from flask import Flask, render_template, request, jsonify
from SingleCntrSimulator import genCntrMasterFxp

app = Flask(__name__, template_folder='../templates', static_folder='../assets')


@app.route('/')
def index():
    '''
    This is the home page of the website, which also returns the counter bits based on counter size.
    '''
    combinedValue = ''  # Initialize the combinedValue variable
    return render_template('index.html', combinedValue=combinedValue)


@app.route('/webapp/BitstoF2P', methods=['POST'])
def bitsToF2P():
    '''
    This recieves counter size, hyper size, counter bits and flavor type from the form to return the f2p value
    it represents.
    '''
    try:
        # Retrieve the form data from the request
        cntrSize = request.form.get('cntr_size')
        hyperSize = request.form.get('hyper_size')
        cntrBits = request.form.get('cntrBits')
        flavor = request.form.get('flavor_type')
        nSystem = request.form.get('fp_type')

        # Call the custom process_form() function
        myCntr = genCntrMasterFxp(cntrSize=int(cntrSize), hyperSize=int(hyperSize), nSystem=str(nSystem), flavor=str(flavor), verbose=[])
        result = myCntr.cntr2num(cntr=str(cntrBits))
        # Return the result as a JSON response
        return jsonify({"result": result})
    except Exception as e:
        # Handle any exceptions that occur during the function execution
        return jsonify({"error": str(e)}), 500


@app.route('/webapp/BitstoF2P', methods=['POST'])
def F2PToBits():
    '''
    This recieves counter size, hyper size, counter bits and flavor type from the form to return the f2p value
    it represents.
    '''
    try:
        # Retrieve the form data from the request
        cntr_size = request.form.get('cntrsize')
        hyper_size = request.form.get('hypersize')
        f2p_value = request.form.get('f2pvalue')
        flavor_type = request.form.get('flavortype')
        fp_type = request.form.get('fptype')
        # Call the custom process_form() function
        cntrValue = float('-inf')
        # Call the custom process_form() function
        myCntr = genCntrMasterFxp(cntrSize=int(cntr_size), hyperSize=int(hyper_size), nSystem=str(fp_type), flavor=str(flavor_type), verbose=[])
        while (f2p_value >= cntrValue):
            cntrValue = myCntr.incCntr(cntrIdx=0, factor=int(1), mult=False, verbose=[])
        # Return the result as a JSON response
        cntr_bits = myCntr.cntrs[0]
        return jsonify({"result": cntr_bits})
    except Exception as e:
        # Handle any exceptions that occur during the function execution
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)