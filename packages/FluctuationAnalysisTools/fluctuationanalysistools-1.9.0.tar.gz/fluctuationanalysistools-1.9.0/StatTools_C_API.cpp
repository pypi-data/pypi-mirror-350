#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>
#include <vector>
#include <random>
#include <iostream>
#include <fstream>


double get_exponential_dist_value(double lambda)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::exponential_distribution<double> dist(1/lambda);
    return dist(gen);
}


double get_gauss_dist_value()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> dist(0.0, 1.0);
    return dist(gen);
}

std::vector<double> get_exp_dist_vector(double lambda, int size){

    std::vector<double> exp_vector;

    for(int i=0; i < size; i++)
        exp_vector.push_back(get_exponential_dist_value(lambda));

    return exp_vector;
}

std::vector<double> get_poisson_thread(std::vector<double> input_vector, double divisor=1){

    std::vector<double> output_vector;

    for (double i:input_vector){
        for (double exp_val:get_exp_dist_vector(divisor / i, ceil(i/divisor))){
            output_vector.push_back(exp_val);
        }
    }

    return output_vector;
}

std::vector<double> cumsum(std::vector<double> input_vector){
    std::vector<double> cumsum_vector(input_vector.size());
    cumsum_vector[0] = input_vector[0];
    for (int i=1; i<input_vector.size(); i++){
        cumsum_vector[i] = cumsum_vector[i-1] + input_vector[i];
    }

    return cumsum_vector;
}

std::vector<double> core(std::vector<double> p_thread_cumsum, std::vector<double> C, std::vector<double> requests)
{
    std::vector<double> waiting_curve;

    for (double c:C)
    {
        int event_done = 0;
        std::vector<double> T_free;
        std::vector<double> T_waiting;
        double T_service = 1.0 / c;

        for (double event:p_thread_cumsum)
        {
            if (event_done == 0){
                T_free.push_back(T_service + event);
                T_waiting.push_back(0.0);
                event_done ++;
            }
            else{
                if (event < T_free.back()){
                    T_waiting.push_back(T_free.back() - event);
                    T_free.push_back(T_service + T_free.back());
                    event_done ++;
                }
                else{
                    T_free.push_back(T_service + event);
                    T_waiting.push_back(0.0);
                    event_done ++;
                }

            }
        }

        double T_waiting_total = 0.0;
        for (double tw:T_waiting){
            T_waiting_total += tw;
        }

        waiting_curve.push_back(T_waiting_total/event_done);
    }

    return waiting_curve;
}

std::vector<double> model(std::vector<double> input_vector, std::vector<double> U, double C0_global=-1.0){

    std::vector<double> poisson_thread = get_poisson_thread(input_vector);

    std::vector<double> p_thread_cumsum = cumsum(poisson_thread);
    std::vector<double> requests;
    double requests_sum = 0.0;

    for (int i=0; i<poisson_thread.size(); i++){
        requests.push_back(1);
        requests_sum += 1.0;
    }

    double C0;

    if (C0_global < 0) {C0 = requests_sum / (p_thread_cumsum.back() - p_thread_cumsum[0]);}
    else {C0 = C0_global;}

    std::vector<double> C;
    for (int i=0; i < U.size(); i++){
        C.push_back(C0/U[i]);
    }

    std::vector<double> curve = core(p_thread_cumsum, C, requests);

    return curve;

}



static PyObject* get_waiting_time(PyObject* self, PyObject* args){

    PyArrayObject* input_vector=NULL;
    PyArrayObject* U=NULL;
    double C0_input;


    if (!PyArg_ParseTuple(args, "O!O!d", &PyArray_Type, &input_vector, &PyArray_Type, &U, &C0_input)){
        PyErr_SetString(PyExc_RuntimeError, "\t[C-API ERROR] Cannot parse input args!");
        Py_XDECREF(input_vector);
        Py_XDECREF(U);
        return NULL;
    }

    if (PyArray_TYPE(input_vector) != NPY_FLOAT64 || PyArray_TYPE(U)!= NPY_FLOAT64)
    {
        PyErr_SetString(PyExc_ValueError, "\t![C-API ERROR] One of the input args is not np.float64!");
        Py_XDECREF(input_vector);
        Py_XDECREF(U);
        return NULL;
    }

    PyObject* curve_output =  PyArray_SimpleNew(PyArray_NDIM(U), PyArray_DIMS(U), NPY_FLOAT64);

    double* output = (double*) PyArray_DATA((PyArrayObject*) curve_output);
    double* input = (double*) PyArray_DATA(input_vector);
    double* u_input = (double*) PyArray_DATA(U);

    int input_vector_length = (int) PyArray_SIZE(input_vector);
    int u_length = (int) PyArray_SIZE(U);

    std::vector<double> vector_for_qss;
    std::vector<double> U_for_qss;

    for (int i=0; i < input_vector_length; i++){
        vector_for_qss.push_back(input[i]);

    }

    for (int i=0; i < u_length; i++){
        U_for_qss.push_back(u_input[i]);
    }

    std::vector<double> curve = model(vector_for_qss, U_for_qss, C0_input);

    for (int i=0; i < u_length; i++){
        output[i] = curve[i];
    }
    //Py_XDECREF(arr);

    return curve_output;



}




void set_item(PyArrayObject* arr, int i, int j, double value){
    PyObject* float_value = PyFloat_FromDouble(value);
    PyArray_SETITEM(arr, (char*)PyArray_GETPTR2(arr, i, j), float_value);
    Py_DECREF(float_value);
}

double get_item(PyArrayObject* arr, int i, int j){
    PyObject* item = PyArray_GETITEM(arr, (char*)PyArray_GETPTR2(arr, i, j));
    double value = PyFloat_AsDouble(item);
    Py_DECREF(item);
    return value;
}


static PyObject* fbm_core(PyObject* self, PyObject* args){
    PyArrayObject* input_array=NULL;
    double H;
    int N;
    PyObject* ret = Py_None;



    if (!PyArg_ParseTuple(args, "O!di", &PyArray_Type, &input_array, &H, &N)){
        PyErr_SetString(PyExc_RuntimeError, "\t[C-API ERROR| FBM] Cannot parse input args!");
        return NULL;
    }

    if (PyArray_TYPE(input_array) != NPY_FLOAT64)
    {
        PyErr_SetString(PyExc_ValueError, "\t![C-API ERROR| FBM] Array has wrong datatype! Only float and integer values are supported!");
        return NULL;
    }

    double* F = (double*) PyArray_DATA((PyArrayObject*) input_array);
    npy_intp first_dim = (npy_intp)PyArray_SHAPE(input_array)[0];
    npy_intp second_dim = (npy_intp)PyArray_SHAPE(input_array)[1];

    // ------------------------- Now the algo itself ----------------------------------

    int n = pow(2.0, N) + 1;

    F[0*second_dim + 0] = get_gauss_dist_value();
    F[0*second_dim + second_dim-1] = get_gauss_dist_value();
    F[(first_dim - 1)*second_dim + 0] = get_gauss_dist_value();
    F[(first_dim - 1)*second_dim + second_dim - 1] = get_gauss_dist_value();

    double min_val = 0.0;
    double max_val = 0.0;

    double value = 0.0;
    double v1, v2, v3, v4 = 0.0;

    for (int k=1; k <= N; k++){
        int m = pow(2, k);
        int fl = floor(n / m);

        int l1 = fl;
        int s = fl * 2;
        int l2 = floor((m - 1) * n / m) + 1;

        for (int i=l1; i < l2; i += s){
            for (int j=l1; j < l2; j += s){

                v1 = get_item(input_array, i - fl, j - fl);
                v2 = get_item(input_array, i - fl, j + fl);
                v3 = get_item(input_array, i + fl, j - fl);
                v4 = get_item(input_array, i + fl, j + fl);

                set_item(input_array, i, j, (v1 + v2 + v3 + v4) / 4);
            }
        }

        for (int i=0; i < n; i += s){
            for (int j=fl; j < l2; j += s){
                value = (get_item(input_array, i, j - fl) + get_item(input_array, i, j + fl)) / 2;
                set_item(input_array, i, j, value);
            }
        }

        for (int j=0; j < n; j += s){
            for (int i=fl; i < l2; i += s){
                value = (get_item(input_array, i - fl, j) + get_item(input_array, i + fl, j)) / 2;
                set_item(input_array, i, j, value);
            }
        }

        for (int i = 0; i <  first_dim; i ++) {
            for (int j = 0; j < second_dim; j ++){

                if (get_item(input_array, i, j) != 0){
                    value = get_item(input_array, i, j);
                    set_item(input_array, i, j, value + pow(0.5, (k * (H - 1))) * get_gauss_dist_value());

                    if (value < min_val){
                        min_val = value;
                    }
                    if (value > max_val){
                        max_val = value;
                    }
                }

            }
        }

    }

    double diff = max_val - min_val;

    for(int i=0; i < first_dim; i ++){
        for (int j=0; j < second_dim; j ++){
            double value = (get_item(input_array, i, j) - min_val) / diff * 255.0;
            set_item(input_array, i, j, value);
        }
    }

    return ret;
}


static PyMethodDef methods[] = {
    {"get_waiting_time", get_waiting_time, METH_VARARGS, "Returns Tw (average waiting time) of given vector."},
    {"fbm_core", fbm_core, METH_VARARGS, "Fractal Brownian Motion core algorithm. Way faster than Python implementation"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "C_StatTools", "Same as MulticoreStatTools but faster", -1, methods
};


PyMODINIT_FUNC
PyInit_C_StatTools(void) {
    import_array();
    PyObject *mod = PyModule_Create(&module);

    return mod;
}


int main() {
    int nd = 2;
    npy_intp dims[] = {1024, 1024};

    PyObject* curve_output =  PyArray_SimpleNew(nd, dims, NPY_FLOAT64);

    fbm_core(Py_None, curve_output);




    // std::vector<double> numbers;
    // std::ifstream inputFile("test_array.txt");        // Input file stream object

    // if (inputFile.good()) {
    //     double current_number;
    //     while (inputFile >> current_number){
    //         numbers.push_back(current_number);
    //     }
    //     inputFile.close();
    // }

    // double* input_pointer = numbers.data();


    // std::vector<double> U = {0.5, 0.6, 0.7, 0.8, 0.9};
    // double* u_pointer = U.data();

    // std::vector<double> curve = model(numbers, U);

    // for(int i =0 ; i < 5; i ++){
    //     std::cout << curve[i] <<std::endl;
    // }

    /*Py_Initialize();
    PyRun_SimpleString("print('Started! ! !')");

    Py_Finalize();*/

    return 0;
}
